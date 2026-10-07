#!/usr/bin/env python3
"""Publish only the explicitly requested 20260809 folder; never delete unverified input."""
import concurrent.futures, csv, hashlib, json, os, re, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

ROOT=Path.cwd()
INPUT='zip/20260809_화곡농장_스프링클러_배관계획_작업정리'
INPUT_TREE='42cc1d080b28e96c968262f8b70aa87bad8bc9d4'
SLUG='20260809-sprinkler-piping-plan'
DEST=Path('public/records')/SLUG
HOME='https://softm.github.io/hwagok-farm/'
CENTRAL='https://softm.github.io/projects/hwagok-farm/'
URL=HOME+'records/'+SLUG+'/'
REPO_URL='https://github.com/softm/hwagok-farm/tree/main/'+DEST.as_posix()
RUN=Path('.archive-run/sprinkler-20260809')
IGNORE={'.DS_Store','Thumbs.db','__MACOSX'}
NORM=lambda s: re.sub(r'\s+',' ',s).strip()

def git(*args): return subprocess.check_output(['git',*args],text=True).strip()
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def files(root):
 for p in sorted(root.rglob('*')):
  if any(x in IGNORE or x.startswith('._') for x in p.relative_to(root).parts): continue
  if p.is_symlink(): raise RuntimeError('Symlink input refused')
  if p.is_file(): yield p

def inventory(root): return [{'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':sha(p)} for p in files(root)]
def verify_local(root,items):
 for f in items:
  p=root/f['path']
  if not p.is_file() or p.stat().st_size!=f['size'] or sha(p)!=f['sha256']: raise RuntimeError('Original differs: '+f['path'])

def get(url):
 if not url.startswith('https://softm.github.io/'): raise RuntimeError('Unexpected origin')
 req=Request(url,headers={'User-Agent':'SOFTM-Archive-Verification','Cache-Control':'no-cache'})
 with urlopen(req,timeout=60) as r:
  if r.status!=200: raise RuntimeError('HTTP '+str(r.status))
  return r.read()

def build():
 RUN.mkdir(parents=True,exist_ok=True)
 if git('rev-parse','HEAD:'+INPUT)!=INPUT_TREE: raise RuntimeError('Uploaded input changed; review required')
 source=Path(INPUT); original=inventory(source)
 html_files=[p for p in source.iterdir() if p.suffix.lower() in ('.html','.htm')]
 if len(html_files)!=1: raise RuntimeError('Ambiguous HTML source')
 entry=html_files[0]; doc=BeautifulSoup(entry.read_text(encoding='utf-8-sig'),'html.parser')
 if not doc.h1 or not doc.find('table'): raise RuntimeError('Expected rendered original HTML')
 title=NORM(doc.h1.get_text(' ',strip=True))
 for node in doc.select('[src],[data-full],link[href]'):
  for attr in ('src','data-full','href'):
   raw=node.get(attr)
   if not raw or raw.startswith(('#','data:')): continue
   u=urlsplit(raw)
   if u.scheme or u.netloc: raise RuntimeError('External resource requires explicit review: '+raw)
   p=(entry.parent/unquote(u.path)).resolve()
   if not p.is_relative_to(source.resolve()) or not p.is_file(): raise RuntimeError('Missing/unsafe relative resource: '+raw)
 image_count=sum(Path(f['path']).suffix.lower()=='.png' for f in original)
 if image_count!=32 or len(original)!=34: raise RuntimeError('Unexpected source inventory')
 for old in Path('public/records').glob('*/archive-manifest.json'):
  m=json.loads(old.read_text())
  if old.parent!=DEST and (m.get('source')==source.name or m.get('input')==INPUT): raise RuntimeError('Existing canonical record requires reconciliation: '+str(old.parent))
 if DEST.exists():
  manifest=DEST/'archive-manifest.json'
  if not manifest.is_file() or json.loads(manifest.read_text()).get('inputTree')!=INPUT_TREE: raise RuntimeError('Existing destination has another source')
 else:
  DEST.mkdir(parents=True)
  for f in original:
   dst=DEST/f['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/f['path'],dst)
 shutil.copy2(entry,DEST/'index.html')
 verify_local(DEST,original)
 if sha(entry)!=sha(DEST/'index.html'): raise RuntimeError('HTML byte preservation failed')
 metadata={'schemaVersion':3,'id':SLUG,'slug':SLUG,'directory':SLUG,'recordPath':DEST.as_posix(),'title':title,'sourceTitle':title,'sourceDocumentTitle':doc.title.get_text(strip=True),'date':'2026-08-09','dateSource':'archive-canonical','titleSource':'archive-canonical','visibility':'public','category':'관수·배관','summary':'스프링클러·배관 계획도, 원본 지도, 치수 보완 도면 및 배관·연결부 심벌. PNG 원본 32개와 HTML·MD 원문 보존.','url':URL,'repoUrl':REPO_URL,'media':{'images':32,'videos':0,'audio':0,'documents':1},'entrySource':entry.name,'entryPolicy':'original-html-byte-exact'}
 write(DEST/'archive.json',metadata)
 originals=original+[{'path':'index.html','size':entry.stat().st_size,'sha256':sha(entry)}]
 manifest={'schemaVersion':3,'source':source.name,'input':INPUT,'inputTree':INPUT_TREE,'metadata':metadata,'originalFileCount':34,'imageCount':32,'originals':original,'files':originals,'entrySource':entry.name,'entrySha256':sha(entry)}
 write(DEST/'archive-manifest.json',manifest)
 with (DEST/'source-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['path','size','sha256']);writer.writeheader();writer.writerows(original)
 page=Path('index.html'); text=page.read_text(encoding='utf-8')
 pattern=re.compile(r'(<script\b[^>]*\bid=[\"\x27]archive-data[\"\x27][^>]*>)(.*?)(</script>)',re.S)
 match=pattern.search(text)
 if not match: raise RuntimeError('Canonical service archive-data not found')
 rows=json.loads(match.group(2))
 if not isinstance(rows,list): raise RuntimeError('Unexpected service catalogue shape')
 rows=[r for r in rows if r.get('dir')!=SLUG and r.get('url')!=URL]
 rows.append({'date':metadata['date'],'kind':metadata['category'],'title':title,'dir':SLUG,'desc':metadata['summary'],'url':URL,'repoUrl':REPO_URL})
 rows.sort(key=lambda r:(r.get('date',''),r.get('title','')),reverse=True)
 content=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\/')
 page.write_text(text[:match.start(2)]+content+text[match.end(2):],encoding='utf-8')
 write(RUN/'build.json',{'input':INPUT,'inputTree':INPUT_TREE,'recordPath':str(DEST),'title':title,'publicCount':len(rows),'originalFiles':len(original),'images':image_count,'entrySha256':sha(entry)})
 print(json.dumps(json.loads((RUN/'build.json').read_text()),ensure_ascii=False))

def downloaded(info):
 url=URL+quote(info['path'],safe='/')+'?verify='+os.environ.get('GITHUB_RUN_ID','local')
 for attempt in range(4):
  try:
   data=get(url)
   if len(data)!=info['size'] or hashlib.sha256(data).hexdigest()!=info['sha256']: raise RuntimeError('Deployed bytes differ: '+info['path'])
   return {'path':info['path'],'status':200,'sha256':info['sha256']}
  except Exception:
   if attempt==3: raise
   time.sleep(10)

def browser_checks(final):
 from playwright.sync_api import sync_playwright
 m=json.loads((DEST/'archive.json').read_text())
 evidence={}
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  ctx=browser.new_context(viewport={'width':1365,'height':900},service_workers='block')
  page=ctx.new_page()
  def visit(url):
   r=page.goto(url,wait_until='domcontentloaded',timeout=60000)
   if not r or r.status!=200: raise RuntimeError('Page did not load: '+url)
   page.wait_for_timeout(2500)
  visit(URL)
  if NORM(page.locator('h1').first.inner_text())!=m['title']: raise RuntimeError('Detail title mismatch')
  page.locator('img[src]').evaluate_all("ns=>ns.forEach(n=>{if(n.getAttribute('src'))n.loading='eager'})")
  images=page.locator('img[src]').evaluate_all("""async ns=>Promise.all(ns.filter(n=>n.getAttribute('src')).map(async n=>{try{await Promise.race([n.decode(),new Promise((_,bad)=>setTimeout(()=>bad(Error('timeout')),30000))]);return {src:n.currentSrc,ok:n.naturalWidth>0}}catch(e){return {src:n.currentSrc,ok:false}}}))""")
  if not images or any(not x['ok'] for x in images): raise RuntimeError('Broken image in original page')
  page.locator('button[data-full]').first.click()
  box=page.locator('.lightbox.open');box.wait_for(state='visible')
  box.locator('img').evaluate('async n=>{await n.decode();if(!n.naturalWidth)throw Error("zoom image missing")}')
  box.locator('.close').click();box.wait_for(state='hidden')
  evidence.update(detail=True,title=m['title'],renderedImages=len(images),uniqueImages=len({x['src'] for x in images}),imageZoom=True)
  page.screenshot(path=str(RUN/'detail-desktop.png'))
  page.set_viewport_size({'width':390,'height':844})
  page.screenshot(path=str(RUN/'detail-mobile.png'))
  evidence['mobileRendered']=page.locator('h1').first.is_visible()
  page.set_viewport_size({'width':1365,'height':900})
  visit(HOME)
  link=page.locator('a').filter(has_text=m['title'])
  if not link.count() or not page.locator('a[href="'+REPO_URL+'"]').count(): raise RuntimeError('Service record/source link missing')
  exact=page.locator('a[href="'+URL+'"]')
  if not exact.count(): raise RuntimeError('Service detail link missing')
  exact.first.click();page.wait_for_url(URL,timeout=30000)
  if NORM(page.locator('h1').first.inner_text())!=m['title']: raise RuntimeError('Service click led to wrong record')
  evidence['serviceHome']=True
  if final:
   visit(CENTRAL)
   page.locator('a[href="'+URL+'"]').first.wait_for(state='visible',timeout=45000)
   if not page.locator('a[href="'+REPO_URL+'"]').count(): raise RuntimeError('Central GitHub record directory link missing')
   if NORM(page.locator('a[href="'+URL+'"]').first.inner_text())!=m['title']: raise RuntimeError('Central title mismatch')
   page.screenshot(path=str(RUN/'central-home.png'),full_page=True)
   page.locator('a[href="'+URL+'"]').first.click();page.wait_for_url(URL,timeout=30000)
   if NORM(page.locator('h1').first.inner_text())!=m['title']: raise RuntimeError('Central click led to wrong record')
   visit('https://softm.github.io/projects/')
   card=page.locator('[data-record="'+CENTRAL+'"]');card.first.wait_for(state='visible',timeout=45000)
   central=json.loads(get('https://softm.github.io/projects/projects.json?verify='+os.getenv('GITHUB_RUN_ID','local')))
   p=next(p for p in central['projects'] if p['repo']=='hwagok-farm')
   public=sum(x.get('visibility')=='public' for x in p['links']); private=sum(x.get('visibility')=='private' for x in p['links'])
   text=card.first.inner_text()
   if '공개 '+str(public) not in text or '비공개 '+str(private) not in text: raise RuntimeError('Rendered central counts are stale')
   page.screenshot(path=str(RUN/'top-projects.png'),full_page=True)
   card.locator('a[href="'+CENTRAL+'"]').first.click();page.wait_for_url(CENTRAL,timeout=30000)
   page.locator('a[href="'+URL+'"]').first.wait_for(state='visible',timeout=45000)
   evidence.update(centralHome=True,topProjects=True,deepLinks=True,publicCount=public,privateCount=private,totalCount=public+private)
  browser.close()
 return evidence

def verify(final=False):
 RUN.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((DEST/'archive-manifest.json').read_text())
 report={'passed':False,'phase':'final' if final else 'live','url':URL,'inputTree':INPUT_TREE,'sourceCommit':git('rev-parse','HEAD'),'images':32,'originalFiles':34}
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: report['byteChecks']=list(ex.map(downloaded,manifest['files']))
  report.update(browser_checks(final));report['passed']=True;report['verifiedAt']=datetime.now(timezone.utc).isoformat()
 finally:
  write(RUN/('final.json' if final else 'live.json'),report)
 print(json.dumps({k:v for k,v in report.items() if k!='byteChecks'},ensure_ascii=False))

def cleanup():
 report=json.loads((RUN/'final.json').read_text())
 required=('passed','detail','imageZoom','mobileRendered','serviceHome','centralHome','topProjects','deepLinks')
 if not all(report.get(k) is True for k in required): raise RuntimeError('Final completion gates not passed')
 subprocess.run(['git','fetch','origin','main'],check=True)
 if git('rev-parse','HEAD')!=git('rev-parse','origin/main'): raise RuntimeError('Concurrent changes: retain input')
 if git('rev-parse','HEAD:'+INPUT)!=INPUT_TREE: raise RuntimeError('Input changed: retain it')
 manifest=json.loads((DEST/'archive-manifest.json').read_text());verify_local(DEST,manifest['files'])
 report['inputCleanup']='verified-originals-preserved-in-record'
 write(Path('reports')/(SLUG+'-completion.json'),report)
 subprocess.run(['git','rm','-r','--',INPUT],check=True)
 subprocess.run(['git','add','--','reports/'+SLUG+'-completion.json'],check=True)
 subprocess.run(['git','commit','-m','archive: retain sprinkler originals and clean fully verified inbox folder'],check=True)
 subprocess.run(['git','push','origin','HEAD:main'],check=True)

if __name__=='__main__':
 command=sys.argv[1] if len(sys.argv)==2 else ''
 if command=='build': build()
 elif command=='live': verify()
 elif command=='final': verify(True)
 elif command=='cleanup': cleanup()
 else: raise SystemExit('build | live | final | cleanup')
