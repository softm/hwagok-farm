#!/usr/bin/env python3
"""Non-destructive ZIP/folder archive builder. Cleanup is a separate proof-gated command."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, shutil, stat, subprocess, tempfile, unicodedata, zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HOME = 'https://softm.github.io/hwagok-farm/'
CENTRAL = 'https://softm.github.io/projects/hwagok-farm/'
REPO = 'softm/hwagok-farm'
POLICY = {
 'projects/archive-deployment/archive_deployment_prompt.md':'ef3988364151b100949510c8e3176d5f0a2df724',
 'projects/archive-deployment/20261005_아카이브배포_ZIP폴더_Workflow_처리기준.md':'0a3a002aa459d1cfb08e721baae9082c22c31c79',
}
IGNORED = {'.DS_Store', 'Thumbs.db', '__MACOSX'}
IMAGES={'.jpg','.jpeg','.png','.webp','.gif','.avif','.svg'}
VIDEOS={'.mp4','.mov','.webm','.m4v'}
AUDIO={'.mp3','.m4a','.wav','.ogg','.flac','.aac'}


def digest(path: Path) -> str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
 return h.hexdigest()

def jwrite(path: Path, value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def relpath(raw: str) -> Path:
 raw=unicodedata.normalize('NFC',raw)
 p=PurePosixPath(raw)
 if not raw or '\\' in raw or '\x00' in raw or p.is_absolute() or any(x in {'..','.git','.github'} or ':' in x for x in p.parts):
  raise ValueError('Unsafe archive path: '+repr(raw))
 return Path(*p.parts)

def entries(root: Path):
 for p in sorted(root.rglob('*')):
  if any(x in IGNORED or x.startswith('._') for x in p.relative_to(root).parts): continue
  if p.is_symlink(): raise ValueError('Symlink is not an archive file: '+str(p))
  if p.is_file(): yield p

def inventory(root: Path):
 return [{'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':digest(p)} for p in entries(root)]

def fingerprint(item: Path):
 if item.is_symlink(): raise ValueError('Symlink inbox item')
 if item.is_file(): return digest(item)
 return hashlib.sha256(json.dumps(inventory(item),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def unpack(item: Path, destination: Path):
 seen=set(); total=0
 if item.is_dir():
  source=((p.relative_to(item).as_posix(),p.stat().st_size,p.open) for p in entries(item))
  for name,size,opener in source:
   dst=destination/relpath(name)
   if dst in seen: raise ValueError('Unicode filename collision')
   seen.add(dst); total+=size
   if size>=100*1024*1024 or total>2*1024**3: raise ValueError('Git/expanded archive size limit exceeded')
   dst.parent.mkdir(parents=True,exist_ok=True)
   with opener('rb') as src, dst.open('wb') as out: shutil.copyfileobj(src,out)
 else:
  with zipfile.ZipFile(item) as z:
   for member in z.infolist():
    p=relpath(member.filename)
    if any(x in IGNORED or x.startswith('._') for x in p.parts): continue
    if member.is_dir(): continue
    mode=member.external_attr>>16
    if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not stat.S_ISREG(mode)): raise ValueError('Non-regular ZIP member')
    total+=member.file_size
    if member.flag_bits&1 or member.file_size>=100*1024*1024 or total>2*1024**3 or len(seen)>=20000: raise ValueError('Unsupported encrypted/oversized ZIP')
    dst=destination/p
    if dst in seen: raise ValueError('Duplicate ZIP path')
    seen.add(dst); dst.parent.mkdir(parents=True,exist_ok=True)
    with z.open(member) as src,dst.open('wb') as out: shutil.copyfileobj(src,out)
 if not seen: raise ValueError('Empty archive input')
 for p in entries(destination):
  if p.name in {'.env','.env.local','id_rsa'}: raise ValueError('Sensitive configuration in public input')
  with p.open('rb') as f: prefix=f.read(128)
  if prefix.startswith(b'version https://git-lfs.github.com/spec/v1'): raise ValueError('LFS pointer is not original media')


def source_root(root: Path):
 while True:
  children=[p for p in root.iterdir() if p.name not in IGNORED]
  if len(children)==1 and children[0].is_dir(): root=children[0]
  else: return root

def choose_entry(root: Path, metadata):
 if metadata.get('entry'):
  chosen=root/relpath(metadata['entry'])
  if not chosen.is_file(): raise ValueError('Declared entry missing')
  return chosen
 # ZIP/folder deployment policy: HTML is the canonical web source.
 # Prefer root index.html, then another HTML file. Markdown is fallback only
 # when no HTML exists at all.
 html=[p for p in entries(root) if p.suffix.lower() in {'.html','.htm'}]
 if html:
  return next((p for p in html if p==root/'index.html'),max(html,key=lambda p:p.stat().st_size))
 md=[p for p in entries(root) if p.suffix.lower()=='.md']
 if md: return max(md,key=lambda p:p.stat().st_size)
 raise ValueError('No narrative HTML/Markdown: retain input rather than generate a filename-only record')

def event_date(metadata, name):
 value=str(metadata.get('date') or metadata.get('authoredAt') or '')
 match=re.search(r'(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)',value or name)
 if not match: raise ValueError('Event date needs explicit metadata; current date is not substituted')
 return dt.date(*map(int,match.groups())).isoformat()

def stable_slug(metadata, name):
 value=str(metadata.get('slug') or metadata.get('id') or Path(name).stem)
 value=unicodedata.normalize('NFC',value).strip().replace(' ','-').replace('_','-')
 if not value or len(value.encode())>230 or not re.fullmatch(r'[\w.-]+',value) or value in {'.','..'}:
  raise ValueError('Provide a safe explicit slug in archive.json')
 return value

def metadata_for(root: Path):
 p=root/'archive.json'
 m=json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
 if not isinstance(m,dict): raise ValueError('archive.json must be an object')
 if m.get('visibility','public')!='public': raise ValueError('Private input must use the private repository')
 return m

def render(root: Path, destination: Path, meta, date, slug):
 chosen=choose_entry(root,meta)
 if chosen.suffix.lower()=='.md':
  doc=subprocess.run(['pandoc','--from=markdown','--to=html5','--standalone',str(chosen)],check=True,capture_output=True,text=True).stdout
 else: doc=chosen.read_text(encoding='utf-8-sig')
 soup=BeautifulSoup(doc,'html.parser')
 if not soup.html:
  soup=BeautifulSoup('<!doctype html><html lang="ko"><head></head><body>'+doc+'</body></html>','html.parser')
 if not soup.head: soup.html.insert(0,soup.new_tag('head'))
 if not soup.body: raise ValueError('Narrative HTML body missing')
 h1=soup.find('h1')
 title=str(meta.get('title') or (h1.get_text(' ',strip=True) if h1 else '') or '')
 if not title: raise ValueError('Narrative has no title; supply archive.json title')
 source_title=re.sub(r'\s+',' ',title).strip()
 title=re.sub(r'^\d{4}[-_.]?\d{2}[-_.]?\d{2}(?:\s*[~–-]\s*(?:\d{4}-?\d{2}-?\d{2}|\d{4}|\d{2}))?[\s_·:-]*','',source_title).strip()
 canonical=date+' '+title
 if not h1:
  h1=soup.new_tag('h1');soup.body.insert(0,h1)
 h1.string=canonical
 if meta.get('dateEnd'):
  date_range=soup.new_tag('p');date_range.string='기록 기간: '+date+' ~ '+meta['dateEnd'];h1.insert_after(date_range)
 if soup.title: soup.title.string=canonical
 else:
  t=soup.new_tag('title');t.string=canonical;soup.head.append(t)
 for base in soup.find_all('base'): base.decompose()
 parent=chosen.relative_to(root).parent.as_posix()
 base=soup.new_tag('base',href='./source/'+('' if parent=='.' else quote(parent,safe='/')+'/'))
 soup.head.insert(0,base)
 canonical_url=HOME+'records/'+quote(slug,safe='')+'/'
 for old in soup.find_all('link',rel='canonical'): old.decompose()
 soup.head.append(soup.new_tag('link',rel='canonical',href=canonical_url))
 if not soup.find('meta',attrs={'name':'viewport'}): soup.head.append(soup.new_tag('meta',attrs={'name':'viewport','content':'width=device-width,initial-scale=1'}))
 # Preserve original narrative and media bytes. Add a compact source inventory.
 style=soup.new_tag('style');style.string='body{max-width:1120px;margin:auto;padding:16px;line-height:1.65}h1{font-size:1.65rem;line-height:1.35}img,video{max-width:100%;height:auto}.archive-sources{overflow-wrap:anywhere}.archive-media{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.archive-media figure{margin:0}'
 soup.head.append(style)
 section=soup.new_tag('section',attrs={'class':'archive-sources'}); heading=soup.new_tag('h2');heading.string='원본 자료';section.append(heading)
 gallery=soup.new_tag('div',attrs={'class':'archive-media'});section.append(gallery)
 listing=soup.new_tag('ul');section.append(listing)
 referenced=set()
 for tag in soup.find_all(['img','video','audio','source']):
  val=tag.get('src')
  if val and not urlsplit(val).scheme and not val.startswith('/'):
   referenced.add((chosen.parent/unquote(urlsplit(val).path)).resolve())
 for p in entries(root):
  link=canonical_url+'source/'+quote(p.relative_to(root).as_posix(),safe='/')
  li=soup.new_tag('li');a=soup.new_tag('a',href=link);a.string=p.relative_to(root).as_posix();li.append(a);listing.append(li)
  ext=p.suffix.lower()
  if p.resolve() not in referenced and ext in IMAGES|VIDEOS|AUDIO:
   fig=soup.new_tag('figure')
   if ext in IMAGES: tag=soup.new_tag('img',src=link,alt=p.name,loading='lazy')
   else: tag=soup.new_tag('video' if ext in VIDEOS else 'audio',src=link,controls='',preload='metadata')
   fig.append(tag);gallery.append(fig)
 nav=soup.new_tag('p')
 for label,url in [('화곡농장 기록 홈',HOME),('중앙 프로젝트 홈',CENTRAL),(slug,'https://github.com/'+REPO+'/tree/main/public/records/'+quote(slug,safe=''))]:
  a=soup.new_tag('a',href=url);a.string=label;nav.append(a);nav.append(' · ')
 soup.body.insert(0,nav);soup.body.append(section)
 (destination/'index.html').write_text(str(soup),encoding='utf-8')
 parsed=BeautifulSoup(str(soup),'html.parser')
 for tag in parsed.find_all(['a','img','video','audio','source']):
  key='href' if tag.name=='a' else 'src'; val=tag.get(key)
  if val and not urlsplit(val).scheme and not val.startswith(('/','#')):
   tag[key]='source/'+('' if parent=='.' else parent+'/')+val
 parsed.find('base').decompose()
 md=subprocess.run(['pandoc','--from=html','--to=gfm'],input=str(parsed),check=True,capture_output=True,text=True).stdout
 (destination/'summary.md').write_text(md,encoding='utf-8')
 return {'id':str(meta.get('id') or slug),'slug':slug,'sourceTitle':source_title,'dateEnd':meta.get('dateEnd'),'date':date,'title':canonical,'userTitle':title,'category':meta.get('category','아카이브'),'summary':meta.get('summary',''),'visibility':'public','url':canonical_url,'repoUrl':'https://github.com/'+REPO+'/tree/main/public/records/'+quote(slug,safe=''),'directory':slug,'recordPath':'public/records/'+slug,'authoredAt':date,'dateSource':'user-specified'}

def verify_files(target: Path, files):
 if not files: raise ValueError('Empty file proof')
 for info in files:
  p=target/relpath(info['path'])
  if not p.is_file() or p.is_symlink() or p.stat().st_size!=info['size'] or digest(p)!=info['sha256']:
   raise ValueError('Missing/changed archive file: '+info['path'])

def build(item: Path, root: Path):
 if any(word in unicodedata.normalize('NFC',item.name) for word in ('비공개','농지증여','경영체','보험','진료','의료','계약서')):
  raise ValueError('Potentially sensitive input: use private archive review, not automatic public publication')
 before=fingerprint(item)
 records=root/'public/records'; records.mkdir(parents=True,exist_ok=True)
 # Keep canonical directories, including legacy hash-shaped slugs, unchanged.
 for manifest in sorted(records.glob('*/archive-manifest.json')):
  old=json.loads(manifest.read_text(encoding='utf-8'))
  if old.get('inputSha256')==before:
   verify_files(manifest.parent,old['files'])
   return {'input':item.relative_to(root).as_posix(),'inputHash':before,'recordPath':manifest.parent.relative_to(root).as_posix(),'slug':manifest.parent.name,'files':old['files'],'metadata':old.get('metadata'),'reused':True}
 with tempfile.TemporaryDirectory() as td:
  stage=Path(td); source=stage/'unpacked';source.mkdir();unpack(item,source); source=source_root(source)
  meta=metadata_for(source); date=event_date(meta,item.name);slug=stable_slug(meta,item.name)
  period=re.search(r'20\d{6}-(\d{2})(\d{2})',item.name)
  if period and not meta.get('dateEnd'): meta['dateEnd']=dt.date(int(date[:4]),int(period[1]),int(period[2])).isoformat()
  if meta.get('dateEnd') and dt.date.fromisoformat(meta['dateEnd'])<dt.date.fromisoformat(date): raise ValueError('Invalid event date range')
  # Exact full file-set deduplication handles a second ZIP without inventing a new slug.
  raw=inventory(source)
  for oldpath in records.iterdir():
   if not oldpath.is_dir(): continue
   if any(all((candidate/f['path']).is_file() and digest(candidate/f['path'])==f['sha256'] for f in raw) for candidate in (oldpath,oldpath/'source')):
    raise ValueError('Existing matching record '+oldpath.name+': requires canonical reconciliation; no duplicate written')
  target=records/slug
  if target.exists(): raise ValueError('Canonical record already exists; preserve it and retain changed input: '+slug)
  draft=stage/'record';draft.mkdir();shutil.copytree(source,draft/'source')
  metadata=render(source,draft,meta,date,slug)
  jwrite(draft/'archive.json',metadata)
  files=inventory(draft);verify_files(draft,files)
  if fingerprint(item)!=before: raise ValueError('Inbox changed during build')
  jwrite(draft/'archive-manifest.json',{'schemaVersion':2,'inputSha256':before,'source':item.name,'metadata':metadata,'policyBlobs':POLICY,'files':files})
  pending=root/'.archive-run/staging'/slug
  pending.parent.mkdir(parents=True,exist_ok=True)
  if pending.exists(): shutil.rmtree(pending)
  shutil.copytree(draft,pending);verify_files(pending,files);os.replace(pending,target)
  return {'input':item.relative_to(root).as_posix(),'inputHash':before,'recordPath':target.relative_to(root).as_posix(),'slug':slug,'files':files,'metadata':metadata,'reused':False}

def build_batch(root=ROOT):
 inbox=root/'zip'; tasks=[];errors=[]
 for item in sorted(inbox.iterdir()) if inbox.is_dir() else []:
  if item.name in IGNORED or item.name.startswith('.') or (item.is_file() and item.suffix.lower()!='.zip'): continue
  try: tasks.append(build(item,root))
  except Exception as error: errors.append({'input':item.name,'error':str(error)})
 plan={'schemaVersion':2,'repository':REPO,'policyBlobs':POLICY,'records':tasks,'errors':errors}
 jwrite(root/'.archive-run/plan.json',plan)
 # Metadata is mandatory before listing a reused legacy record; do not invent it.
 if any(not task.get('metadata') for task in tasks): errors.append({'error':'Legacy manifest needs metadata reconciliation; input retained'})
 if errors: jwrite(root/'.archive-run/plan.json',plan);raise ValueError('Inbox build incomplete; see .archive-run/plan.json')
 if tasks:
  page=root/'index.html';soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser');data=soup.find('script',id='archive-data')
  if not data: raise ValueError('Service home catalog missing')
  catalog=json.loads(data.string);by={r['dir']:r for r in catalog}
  for task in tasks:
   m=task['metadata'];by[m['slug']]={'date':m['date'],'kind':m['category'],'title':m['title'],'dir':m['slug'],'desc':m['summary'],'url':m['url'],'repoUrl':m['repoUrl']}
  data.string=json.dumps(sorted(by.values(),key=lambda r:(r['date'],r['title']),reverse=True),ensure_ascii=False).replace('</','<\\/')
  page.write_text(str(soup),encoding='utf-8')
 if os.getenv('GITHUB_OUTPUT'):
  with open(os.environ['GITHUB_OUTPUT'],'a') as out: out.write('count='+str(len(tasks))+'\n')
 print(json.dumps({'prepared':len(tasks),'errors':len(errors),'inboxDeleted':False},ensure_ascii=False))
 return plan

if __name__=='__main__': build_batch()
