#!/usr/bin/env python3
"""Non-destructive ZIP/folder archive builder. Cleanup is a separate proof-gated command."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, html, json, os, re, shutil, stat, subprocess, tempfile, unicodedata, zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HOME = 'https://softm.github.io/hwagok-farm/'
CENTRAL = 'https://softm.github.io/projects/hwagok-farm/'
REPO = 'softm/hwagok-farm'
POLICY = {
 'projects/archive-deployment/archive_deployment_prompt.md':'9413aa3e970bbc18111f4bcf37418b7faba4e3d6',
 'projects/archive-deployment/20261005_아카이브배포_ZIP폴더_Workflow_처리기준.md':'dd087e26ca3429a32a46d8292064c522959c7458',
}
IGNORED = {'.DS_Store', 'Thumbs.db', '__MACOSX'}
IMAGES={'.jpg','.jpeg','.png','.webp','.gif','.avif','.svg'}
VIDEOS={'.mp4','.mov','.webm','.m4v'}
AUDIO={'.mp3','.m4a','.wav','.ogg','.flac','.aac'}
# SOFTM-archive-policy-v2: 최신 중앙 정책 blob을 검토·고정하고 입력 형식 분류를 유지 (2026-10-15)


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
  if chosen.suffix.lower() in {'.html','.htm'}: return chosen
 # SOFTM-archive-entry-fallback START: 원본 HTML을 우선하되 없으면 안전한 MD/TXT/미디어 HTML 생성을 허용 (2026-10-15)
 html=[p for p in entries(root) if p.suffix.lower() in {'.html','.htm'}]
 if not html: return None
 root_html=[p for p in html if p.parent==root]
 if root/'index.html' in html:
  return root/'index.html'
 if root_html:
  return max(root_html,key=lambda p:p.stat().st_size)
 return max(html,key=lambda p:p.stat().st_size)

def choose_text(root: Path, suffixes):
 candidates=[p for p in entries(root) if p.suffix.lower() in suffixes]
 if not candidates: return None
 preferred=[p for p in candidates if p.stem.lower() in {'readme','summary','index'}]
 top=[p for p in candidates if p.parent==root]
 return max(preferred or top or candidates,key=lambda p:p.stat().st_size)

def markdown_title(text: str, fallback: str):
 match=re.search(r'^\s*#\s+(.+?)\s*$',text,re.M)
 value=match.group(1) if match else fallback
 return re.sub(r'[`*_\[\]]','',value).strip() or fallback

def sanitize_fragment(fragment: str):
 soup=BeautifulSoup(fragment,'html.parser')
 for tag in soup.find_all(['script','iframe','object','embed']): tag.decompose()
 for tag in soup.find_all(True):
  for attr in list(tag.attrs):
   if attr.lower().startswith('on'): del tag.attrs[attr]
  for attr in ('href','src'):
   value=str(tag.attrs.get(attr,'')).strip()
   if not value: continue
   parsed=urlsplit(value)
   if value.startswith('//') or (parsed.scheme and parsed.scheme.lower() not in {'http','https','mailto'}):
    del tag.attrs[attr]
 return str(soup)

def attachment_html(root: Path):
 blocks=[]
 for path in entries(root):
  rel=path.relative_to(root).as_posix(); ext=path.suffix.lower()
  if ext in {'.html','.htm','.md','.markdown','.txt','.log','.json'}: continue
  target=html.escape(rel,quote=True); label=html.escape(rel)
  if ext in IMAGES:
   blocks.append(f'<figure><a href="{target}" target="_blank" rel="noopener"><img loading="lazy" src="{target}" alt="{label}"></a><figcaption>{label} · <a href="{target}" download>원본 다운로드</a></figcaption></figure>')
  elif ext in VIDEOS:
   blocks.append(f'<figure><video controls preload="metadata" src="{target}"></video><figcaption>{label} · <a href="{target}" download>원본 다운로드</a></figcaption></figure>')
  elif ext in AUDIO:
   blocks.append(f'<figure><audio controls preload="metadata" src="{target}"></audio><figcaption>{label} · <a href="{target}" download>원본 다운로드</a></figcaption></figure>')
  elif ext=='.pdf':
   blocks.append(f'<article class="file"><strong>{label}</strong><iframe title="{label}" loading="lazy" src="{target}"></iframe><p><a href="{target}" target="_blank" rel="noopener">원본 열기</a> · <a href="{target}" download>다운로드</a></p></article>')
  else:
   blocks.append(f'<p class="file"><a href="{target}" target="_blank" rel="noopener">{label}</a> · <a href="{target}" download>다운로드</a></p>')
 return '\n'.join(blocks)

def generated_shell(title: str, date: str, body: str, attachments: str):
 heading=html.escape(title); shown_date=html.escape(date)
 extra=f'<hr><h2>첨부 자료</h2>{attachments}' if attachments else ''
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{heading}</title><style>body{{max-width:980px;margin:40px auto;padding:0 20px;font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;line-height:1.72;color:#202923}}nav{{display:flex;gap:14px;flex-wrap:wrap}}a{{color:#165c3b}}img,video,iframe{{display:block;max-width:100%;height:auto}}audio{{width:100%}}iframe{{width:100%;height:min(72vh,760px);border:1px solid #ccd3ce}}figure,.file{{margin:24px 0;padding:14px;border:1px solid #d8ddd9;border-radius:12px}}figcaption{{margin-top:8px;font-size:.9rem;word-break:break-all}}pre{{overflow:auto;white-space:pre-wrap;word-break:break-word;background:#f4f6f4;padding:16px;border-radius:10px}}table{{display:block;width:100%;overflow:auto;border-collapse:collapse}}th,td{{border:1px solid #d8ddd9;padding:7px 10px}}</style></head><body><header><nav><a href="{HOME}">프로젝트 홈</a><a href="{CENTRAL}">중앙 프로젝트 홈</a></nav><h1>{heading}</h1><p>{shown_date}</p></header><main>{body}{extra}</main></body></html>'''

def generate_entry(root: Path, meta, input_name: str, date: str):
 fallback=str(meta.get('sourceTitle') or meta.get('title') or Path(input_name).stem)
 declared=root/relpath(meta['entry']) if meta.get('entry') else None
 markdown=declared if declared and declared.suffix.lower() in {'.md','.markdown'} else choose_text(root,{'.md','.markdown'})
 text_file=declared if declared and declared.suffix.lower() in {'.txt','.log'} else choose_text(root,{'.txt','.log'})
 attachments=attachment_html(root)
 if markdown:
  raw=markdown.read_text(encoding='utf-8',errors='replace')
  source_title=markdown_title(raw,fallback)
  body=subprocess.run(['pandoc','--from=gfm-raw_html','--to=html5'],input=raw,check=True,capture_output=True,text=True).stdout
  source_link=html.escape(markdown.relative_to(root).as_posix(),quote=True)
  body=sanitize_fragment(body)+f'<p><a href="{source_link}" download>원본 Markdown 다운로드</a></p>'
  return generated_shell(source_title,date,body,attachments),source_title,'markdown-generated',markdown
 if text_file:
  raw=text_file.read_text(encoding='utf-8',errors='replace');source_title=fallback
  source_link=html.escape(text_file.relative_to(root).as_posix(),quote=True)
  body=f'<pre>{html.escape(raw)}</pre><p><a href="{source_link}" download>원본 텍스트 다운로드</a></p>'
  return generated_shell(source_title,date,body,attachments),source_title,'text-generated',text_file
 listing=''.join(f'<li><a href="{html.escape(p.relative_to(root).as_posix(),quote=True)}">{html.escape(p.relative_to(root).as_posix())}</a></li>' for p in entries(root))
 body='<p>HTML·Markdown·텍스트 본문이 없어 확보된 미디어·문서 목록으로 만든 보기 페이지입니다.</p><ul>'+listing+'</ul>'
 return generated_shell(fallback,date,body,attachments),fallback,'media-generated',None
 # SOFTM-archive-entry-fallback END: 원본 HTML을 우선하되 없으면 안전한 MD/TXT/미디어 HTML 생성을 허용 (2026-10-15)

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

def render(root: Path, destination: Path, meta, date, slug, item: Path):
 # SOFTM-inbox-list-title START: 입력 이름 목록 제목과 원본 문서 제목을 분리 (2026-10-15)
 input_raw=item.name
 input_name=unicodedata.normalize('NFC',input_raw)
 input_kind='folder' if item.is_dir() else 'zip'
 explicit_list_title=str(meta.get('listTitle') or '').strip()
 list_title=explicit_list_title or input_name
 title_source='user-list-title' if explicit_list_title else 'inbox-name'
 chosen=choose_entry(root,meta)
 if chosen:
  # 정상 원본 HTML은 제목 주입 없이 바이트 그대로 배포한다.
  shutil.copy2(chosen,destination/'index.html')
  doc=chosen.read_text(encoding='utf-8-sig')
  soup=BeautifulSoup(doc,'html.parser');h1=soup.find('h1');title_tag=soup.find('title')
  source_title=str(meta.get('sourceDocumentTitle') or (h1.get_text(' ',strip=True) if h1 else '') or (title_tag.get_text(' ',strip=True) if title_tag else '') or meta.get('sourceTitle') or chosen.stem)
  source_title=re.sub(r'\s+',' ',source_title).strip()
  summary=subprocess.run(['pandoc','--from=html','--to=gfm'],input=doc,check=True,capture_output=True,text=True).stdout
  entry_type='html-source';entry_policy='html-exact-v2';entry_source=chosen;generated=False
 else:
  document,source_title,entry_type,entry_source=generate_entry(root,meta,input_name,date)
  (destination/'index.html').write_text(document,encoding='utf-8')
  if entry_source and entry_source.suffix.lower() in {'.md','.markdown'}: summary=entry_source.read_text(encoding='utf-8',errors='replace')
  elif entry_source: summary='# '+source_title+'\n\n```text\n'+entry_source.read_text(encoding='utf-8',errors='replace')+'\n```\n'
  else: summary='# '+source_title+'\n\n본문 원자료가 없어 확보된 미디어·문서 목록으로 보기 페이지를 생성했습니다.\n'
  entry_policy='generated-html-fallback-v1';generated=True
 summary_path=destination/('archive-summary.md' if (root/'summary.md').is_file() else 'summary.md')
 summary_path.write_text(summary,encoding='utf-8')
 canonical_url=HOME+'records/'+quote(slug,safe='')+'/'
 source_sha=digest(entry_source) if entry_source else None
 metadata={'id':str(meta.get('id') or slug),'slug':slug,'inputName':input_name,'inputNameRaw':input_raw,'inputKind':input_kind,'listTitle':list_title,'title':list_title,'label':list_title,'titleSource':title_source,'sourceTitle':source_title,'sourceDocumentTitle':source_title,'userTitle':list_title,'dateEnd':meta.get('dateEnd'),'date':date,'category':meta.get('category','아카이브'),'summary':meta.get('summary',''),'visibility':'public','url':canonical_url,'repoUrl':'https://github.com/'+REPO+'/tree/main/public/records/'+quote(slug,safe=''),'directory':slug,'recordPath':'public/records/'+slug,'authoredAt':date,'dateSource':'user-specified','entrySource':entry_source.relative_to(root).as_posix() if entry_source else 'generated','entryType':entry_type,'entryPolicy':entry_policy,'generatedHtml':generated,'sourceSha256':source_sha,'entrySha256':digest(destination/'index.html'),'rendererVersion':'archive-inbox-2026-10-15.1','summaryPath':summary_path.relative_to(destination).as_posix()}
 return metadata
 # SOFTM-inbox-list-title END: 입력 이름 목록 제목과 원본 문서 제목을 분리 (2026-10-15)

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
  draft=stage/'record';draft.mkdir()
  # Preserve the extracted ZIP/folder tree at the record root so the original
  # HTML keeps its relative image/media/style/script references.
  for p in entries(source):
   rel=p.relative_to(source); dst=draft/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dst)
  # Keep a source mirror as provenance while the root tree remains directly deployable.
  shutil.copytree(source,draft/'source')
  metadata=render(source,draft,meta,date,slug,item)
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
   m=task['metadata'];by[m['slug']]={'date':m['date'],'kind':m['category'],'title':m['listTitle'],'dir':m['slug'],'desc':m['summary'],'url':m['url'],'repoUrl':m['repoUrl'],'inputName':m['inputName'],'inputKind':m['inputKind'],'listTitle':m['listTitle'],'titleSource':m['titleSource'],'sourceTitle':m['sourceTitle']}
  data.string=json.dumps(sorted(by.values(),key=lambda r:(r['date'],r['title']),reverse=True),ensure_ascii=False).replace('</','<\\/')
  page.write_text(str(soup),encoding='utf-8')
 if os.getenv('GITHUB_OUTPUT'):
  with open(os.environ['GITHUB_OUTPUT'],'a') as out: out.write('count='+str(len(tasks))+'\n')
 print(json.dumps({'prepared':len(tasks),'errors':len(errors),'inboxDeleted':False},ensure_ascii=False))
 return plan

if __name__=='__main__': build_batch()
