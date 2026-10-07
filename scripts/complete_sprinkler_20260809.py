#!/usr/bin/env python3
"""Publish only the requested folder; verify every original before inbox cleanup."""
import concurrent.futures, csv, hashlib, html, json, os, re, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
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
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def files(root):
 for p in sorted(root.rglob('*')):
  if any(x in IGNORE or x.startswith('._') for x in p.relative_to(root).parts):continue
  if p.is_symlink():raise RuntimeError('Symlink refused')
  if p.is_file():yield p
def inventory(root):return [{'path':p.relative_to(root).as_posix(),'size':p.stat().st_size,'sha256':sha(p)} for p in files(root)]
def verify_local(root,items):
 for f in items:
  p=root/f['path']
  if not p.is_file() or p.stat().st_size!=f['size'] or sha(p)!=f['sha256']:raise RuntimeError('Original differs: '+f['path'])
def get(url):
 if not url.startswith('https://softm.github.io/'):raise RuntimeError('Unexpected origin')
 with urlopen(Request(url,headers={'User-Agent':'SOFTM-Archive-Verification','Cache-Control':'no-cache'}),timeout=60) as r:
  if r.status!=200:raise RuntimeError('HTTP '+str(r.status))
  return r.read()
def media_viewer(original,title):
 groups={}
 for item in original:groups.setdefault(item['sha256'],[]).append(item)
 body=['<p><a href="./">본문</a> · <a href="'+HOME+'">화곡농장</a> · <a href="'+CENTRAL+'">프로젝트 홈</a></p><h1>'+html.escape(title)+' · 전체 원본</h1><p>원본 경로는 모두 보존하며 같은 내용의 파일은 한 번 미리보기합니다.</p>']
 for group in groups.values():
  item=group[0];name=item['path'];q=html.escape(quote(name,safe='/'),quote=True);ext=Path(name).suffix.lower()
  links=' · '.join('<a href="'+html.escape(quote(x['path'],safe='/'),quote=True)+'" target="_blank" rel="noopener">'+html.escape(x['path'])+'</a>' for x in group)
  if ext in {'.png','.jpg','.jpeg','.webp','.gif'}:preview='<button class="zoom" data-src="'+q+'"><img src="'+q+'" loading="lazy" alt="'+html.escape(name,quote=True)+'"></button>'
  elif ext=='.pdf':preview='<iframe src="'+q+'" title="PDF 계획도 미리보기" loading="eager"></iframe>'
  elif ext in {'.md','.txt'}:preview='<details><summary>텍스트 원문 펼치기</summary><pre>'+html.escape((DEST/name).read_text(encoding='utf-8-sig'))+'</pre></details>'
  else:preview=''
  body.append('<section><h2>'+html.escape(Path(name).name)+'</h2>'+preview+'<p>'+links+'</p><small>'+str(item['size'])+' bytes · SHA-256 '+item['sha256']+'</small></section>')
 body.append('<dialog id="viewer"><button id="close">닫기</button><img id="large" alt="원본 확대"><p><button id="prev">이전</button> <a id="original" target="_blank" rel="noopener">원본 열기</a> <button id="next">다음</button></p></dialog>')
 script="const vs=[...document.querySelectorAll('.zoom')],d=document.querySelector('#viewer');let at=0;function show(i){at=(i+vs.length)%vs.length;document.querySelector('#large').src=vs[at].dataset.src;document.querySelector('#original').href=vs[at].dataset.src;if(!d.open)d.showModal()}vs.forEach((x,i)=>x.onclick=()=>show(i));document.querySelector('#close').onclick=()=>d.close();document.querySelector('#prev').onclick=()=>show(at-1);document.querySelector('#next').onclick=()=>show(at+1);"
 return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' · 전체 원본</title><style>body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:auto;padding:18px;color:#183d2c}h1{font-size:24px}h2{font-size:17px;overflow-wrap:anywhere}section{border-top:1px solid #ccd9d1;padding:20px 0}a,small{overflow-wrap:anywhere}img{max-width:100%;max-height:650px;object-fit:contain}button.zoom{display:block;border:0;background:#eef2ef;width:100%;cursor:zoom-in}iframe{width:100%;height:650px;border:1px solid #ccc}pre{white-space:pre-wrap;max-height:400px;overflow:auto;background:#f1f4f2;padding:12px}dialog{max-width:95vw;max-height:96vh}dialog img{max-height:75vh}dialog::backdrop{background:#000b}</style>'+''.join(body)+'<script>'+script+'</script></html>'
def build():
 RUN.mkdir(parents=True,exist_ok=True)
 if git('rev-parse','HEAD:'+INPUT)!=INPUT_TREE:raise RuntimeError('Uploaded input changed; review required')
 source=Path(INPUT);original=inventory(source)
 hs=[p for p in source.iterdir() if p.suffix.lower() in {'.html','.htm'}]
 if len(hs)!=1:raise RuntimeError('Ambiguous HTML source')
 entry=hs[0];doc=BeautifulSoup(entry.read_text(encoding='utf-8-sig'),'html.parser')
 if not doc.h1 or not doc.find('table'):raise RuntimeError('Expected rendered original HTML')
 title=NORM(doc.h1.get_text(' ',strip=True))
 for node in doc.select('[src],[data-full],link[href]'):
  for attr in ('src','data-full','href'):
   raw=node.get(attr)
   if not raw or raw.startswith(('#','data:')):continue
   u=urlsplit(raw)
   if u.scheme or u.netloc:raise RuntimeError('External resource requires review: '+raw)
   p=(entry.parent/unquote(u.path)).resolve()
   if not p.is_relative_to(source.resolve()) or not p.is_file():raise RuntimeError('Missing/unsafe resource: '+raw)
 imgs=[f for f in original if Path(f['path']).suffix.lower()=='.png'];pdfs=[f for f in original if Path(f['path']).suffix.lower()=='.pdf']
 if len([f for f in imgs if f['path'].startswith('images/')])!=32:raise RuntimeError('Source HTML gallery inventory differs')
 for old in Path('public/records').glob('*/archive-manifest.json'):
  m=json.loads(old.read_text())
  if old.parent!=DEST and (m.get('source')==source.name or m.get('input')==INPUT):raise RuntimeError('Existing canonical requires reconciliation: '+str(old.parent))
 if DEST.exists():
  p=DEST/'archive-manifest.json'
  if not p.is_file() or json.loads(p.read_text()).get('inputTree')!=INPUT_TREE:raise RuntimeError('Existing destination has another source')
 else:
  DEST.mkdir(parents=True)
  for f in original:
   p=DEST/f['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/f['path'],p)
 shutil.copy2(entry,DEST/'index.html');verify_local(DEST,original)
 if sha(entry)!=sha(DEST/'index.html'):raise RuntimeError('HTML preservation failed')
 metadata={'schemaVersion':3,'id':SLUG,'slug':SLUG,'directory':SLUG,'recordPath':str(DEST),'title':title,'sourceTitle':title,'sourceDocumentTitle':doc.title.get_text(strip=True),'date':'2026-08-09','dateSource':'archive-canonical','titleSource':'archive-canonical','visibility':'public','category':'관수·배관','summary':'스프링클러·배관 계획도, 치수 보완 도면 및 연결부 심벌. HTML·MD와 images/·원본이미지/의 모든 원본 및 PDF 보존.','url':URL,'repoUrl':REPO_URL,'attachmentsUrl':URL+'media.html','media':{'images':len(imgs),'uniqueImages':len({f['sha256'] for f in imgs}),'pdf':len(pdfs),'videos':0,'audio':0},'entrySource':entry.name,'entryPolicy':'original-html-byte-exact'}
 write(DEST/'archive.json',metadata)
 (DEST/'media.html').write_text(media_viewer(original,title),encoding='utf-8')
 deployed=original+[{'path':'index.html','size':entry.stat().st_size,'sha256':sha(entry)},{'path':'media.html','size':(DEST/'media.html').stat().st_size,'sha256':sha(DEST/'media.html')}]
 manifest={'schemaVersion':3,'source':source.name,'input':INPUT,'inputTree':INPUT_TREE,'metadata':metadata,'originalFileCount':len(original),'imageCount':len(imgs),'uniqueImageCount':len({f['sha256'] for f in imgs}),'pdfCount':len(pdfs),'originals':original,'files':deployed,'entrySource':entry.name,'entrySha256':sha(entry)}
 write(DEST/'archive-manifest.json',manifest)
 with (DEST/'source-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['path','size','sha256']);w.writeheader();w.writerows(original)
 p=Path('index.html');text=p.read_text(encoding='utf-8');match=re.search(r'(<script\b[^>]*\bid=[\"\x27]archive-data[\"\x27][^>]*>)(.*?)(</script>)',text,re.S)
 if not match:raise RuntimeError('Canonical service catalogue missing')
 rows=json.loads(match[2]);assert isinstance(rows,list)
 rows=[r for r in rows if r.get('dir')!=SLUG and r.get('url')!=URL]
 rows.append({'date':metadata['date'],'kind':metadata['category'],'title':title,'dir':SLUG,'desc':metadata['summary'],'url':URL,'repoUrl':REPO_URL,'attachmentsUrl':URL+'media.html'})
 rows.sort(key=lambda r:(r.get('date',''),r.get('title','')),reverse=True)
 content=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 text=text[:match.start(2)]+content+text[match.end(2):]
 if 'id="sprinkler-originals"' not in text:text=text.replace('</main>','<p id="sprinkler-originals"><a href="'+URL+'media.html">2026-08-09 스프링클러 계획 · 전체 원본 이미지·PDF 보기</a></p></main>',1)
 p.write_text(text,encoding='utf-8')
 write(RUN/'build.json',{'input':INPUT,'inputTree':INPUT_TREE,'recordPath':str(DEST),'title':title,'publicCount':len(rows),'originalFiles':len(original),'images':len(imgs),'uniqueImages':len({f['sha256'] for f in imgs}),'pdf':len(pdfs),'entrySha256':sha(entry)})
 print((RUN/'build.json').read_text())
def downloaded(info):
 url=URL+quote(info['path'],safe='/')+'?verify='+os.getenv('GITHUB_RUN_ID','local')
 for attempt in range(4):
  try:
   data=get(url)
   if len(data)!=info['size'] or hashlib.sha256(data).hexdigest()!=info['sha256']:raise RuntimeError('Deployed bytes differ: '+info['path'])
   return {'path':info['path'],'status':200,'sha256':info['sha256']}
  except Exception:
   if attempt==3:raise
   time.sleep(10)
def browser_checks(final):
 from playwright.sync_api import sync_playwright
 m=json.loads((DEST/'archive.json').read_text());evidence={}
 with sync_playwright() as pw:
  browser=pw.chromium.launch();ctx=browser.new_context(viewport={'width':1365,'height':900},service_workers='block');page=ctx.new_page()
  def visit(url):
   r=page.goto(url,wait_until='domcontentloaded',timeout=60000)
   if not r or r.status!=200:raise RuntimeError('Page did not load: '+url)
   page.wait_for_timeout(2500)
  def images():
   page.locator('img[src]').evaluate_all("ns=>ns.forEach(n=>{if(n.getAttribute('src'))n.loading='eager'})")
   result=page.locator('img[src]').evaluate_all("""async ns=>Promise.all(ns.filter(n=>n.getAttribute('src')).map(async n=>{try{await Promise.race([n.decode(),new Promise((_,bad)=>setTimeout(()=>bad(Error('timeout')),30000))]);return {src:n.currentSrc,ok:n.naturalWidth>0}}catch(e){return {src:n.currentSrc,ok:false}}}))""")
   if not result or any(not x['ok'] for x in result):raise RuntimeError('Broken viewer image')
   return result
  visit(URL)
  if NORM(page.locator('h1').first.inner_text())!=m['title']:raise RuntimeError('Detail title mismatch')
  result=images();page.locator('button[data-full]').first.click();box=page.locator('.lightbox.open');box.wait_for(state='visible')
  box.locator('img').evaluate('async n=>{await n.decode();if(!n.naturalWidth)throw Error("zoom missing")}')
  box.locator('.close').click();box.wait_for(state='hidden')
  evidence.update(detail=True,title=m['title'],renderedImages=len(result),imageZoom=True)
  page.screenshot(path=str(RUN/'detail-desktop.png'));page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(RUN/'detail-mobile.png'))
  evidence['mobileRendered']=page.locator('h1').first.is_visible();page.set_viewport_size({'width':1365,'height':900})
  pdf_responses=[]
  page.on('response',lambda r:pdf_responses.append({'url':r.url,'status':r.status}) if '.pdf' in unquote(r.url).lower() else None)
  visit(URL+'media.html');all_images=images()
  if len(all_images)!=m['media']['uniqueImages']:raise RuntimeError('Additional original images not visible')
  if page.locator('iframe').count()!=m['media']['pdf']:raise RuntimeError('PDF viewer missing')
  for frame in page.locator('iframe').all():frame.scroll_into_view_if_needed();page.wait_for_timeout(2000)
  if m['media']['pdf'] and not any(r['status']==200 for r in pdf_responses):raise RuntimeError('PDF viewer response missing')
  page.screenshot(path=str(RUN/'pdf-viewer.png'))
  evidence.update(allOriginalsViewer=True,uniqueImagesRendered=len(all_images),pdfViewerResponses=pdf_responses)
  visit(HOME)
  if not page.locator('a[href="'+REPO_URL+'"]').count():raise RuntimeError('Service source link missing')
  exact=page.locator('a[href="'+URL+'"]');exact.first.wait_for(state='visible',timeout=45000);exact.first.click();page.wait_for_url(URL,timeout=30000)
  if NORM(page.locator('h1').first.inner_text())!=m['title']:raise RuntimeError('Service click led to wrong record')
  evidence['serviceHome']=True
  if final:
   visit(CENTRAL);link=page.locator('a[href="'+URL+'"]');link.first.wait_for(state='visible',timeout=45000)
   if not page.locator('a[href="'+REPO_URL+'"]').count():raise RuntimeError('Central source link missing')
   if NORM(link.first.inner_text())!=m['title']:raise RuntimeError('Central title mismatch')
   page.screenshot(path=str(RUN/'central-home.png'),full_page=True);link.first.click();page.wait_for_url(URL,timeout=30000)
   if NORM(page.locator('h1').first.inner_text())!=m['title']:raise RuntimeError('Central click led to wrong record')
   visit('https://softm.github.io/projects/');card=page.locator('[data-record="'+CENTRAL+'"]');card.first.wait_for(state='visible',timeout=45000)
   data=json.loads(get('https://softm.github.io/projects/projects.json?verify='+os.getenv('GITHUB_RUN_ID','local')));p=next(p for p in data['projects'] if p['repo']=='hwagok-farm')
   public=sum(x.get('visibility')=='public' for x in p['links']);private=sum(x.get('visibility')=='private' for x in p['links']);text=card.first.inner_text()
   if '공개 '+str(public) not in text or '비공개 '+str(private) not in text:raise RuntimeError('Rendered central counts are stale')
   page.screenshot(path=str(RUN/'top-projects.png'),full_page=True);card.locator('a[href="'+CENTRAL+'"]').first.click();page.wait_for_url(CENTRAL,timeout=30000)
   page.locator('a[href="'+URL+'"]').first.wait_for(state='visible',timeout=45000)
   evidence.update(centralHome=True,topProjects=True,deepLinks=True,publicCount=public,privateCount=private,totalCount=public+private)
  browser.close()
 return evidence
def verify(final=False):
 RUN.mkdir(parents=True,exist_ok=True);m=json.loads((DEST/'archive-manifest.json').read_text())
 report={'passed':False,'phase':'final' if final else 'live','url':URL,'attachmentsUrl':URL+'media.html','inputTree':INPUT_TREE,'sourceCommit':git('rev-parse','HEAD'),'images':m['imageCount'],'uniqueImages':m['uniqueImageCount'],'pdf':m['pdfCount'],'originalFiles':m['originalFileCount']}
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:report['byteChecks']=list(ex.map(downloaded,m['files']))
  report.update(browser_checks(final));report['passed']=True;report['verifiedAt']=datetime.now(timezone.utc).isoformat()
 finally:write(RUN/('final.json' if final else 'live.json'),report)
 print(json.dumps({k:v for k,v in report.items() if k!='byteChecks'},ensure_ascii=False))
def cleanup():
 report=json.loads((RUN/'final.json').read_text());required=('passed','detail','imageZoom','mobileRendered','allOriginalsViewer','serviceHome','centralHome','topProjects','deepLinks')
 if not all(report.get(k) is True for k in required):raise RuntimeError('Final gates not passed')
 subprocess.run(['git','fetch','origin','main'],check=True)
 if git('rev-parse','HEAD')!=git('rev-parse','origin/main'):raise RuntimeError('Concurrent changes: retain input')
 if git('rev-parse','HEAD:'+INPUT)!=INPUT_TREE:raise RuntimeError('Input changed: retain it')
 m=json.loads((DEST/'archive-manifest.json').read_text());verify_local(DEST,m['files'])
 report['inputCleanup']='verified-originals-preserved-in-record';write(Path('reports')/(SLUG+'-completion.json'),report)
 subprocess.run(['git','rm','-r','--',INPUT],check=True);subprocess.run(['git','add','--','reports/'+SLUG+'-completion.json'],check=True)
 subprocess.run(['git','commit','-m','archive: retain sprinkler originals and clean fully verified inbox folder'],check=True);subprocess.run(['git','push','origin','HEAD:main'],check=True)
if __name__=='__main__':
 command=sys.argv[1] if len(sys.argv)==2 else ''
 if command=='build':build()
 elif command=='live':verify()
 elif command=='final':verify(True)
 elif command=='cleanup':cleanup()
 else:raise SystemExit('build | live | final | cleanup')
