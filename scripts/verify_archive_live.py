#!/usr/bin/env python3
"""Verify actual public bytes, browser rendering and navigation before cleanup."""
from __future__ import annotations
import concurrent.futures, hashlib, json, os, sys, time
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
from playwright.sync_api import sync_playwright
from archive_inbox import ROOT, HOME, CENTRAL, jwrite
from archive_completion import RUN, load_plan, proof_base, read_proof, api


def download_check(task):
 url,info=task
 if urlsplit(url).netloc!='softm.github.io' or not urlsplit(url).path.startswith('/hwagok-farm/records/'):
  raise RuntimeError('Refusing non-project source URL')
 for attempt in range(4):
  try:
   h=hashlib.sha256();size=0
   with urlopen(Request(url+'?archive_verify='+os.getenv('GITHUB_RUN_ID','local'),headers={'User-Agent':'SOFTM-Archive-Verifier','Cache-Control':'no-cache'}),timeout=60) as response:
    if response.status!=200: raise RuntimeError('Original HTTP status is not 200')
    for part in iter(lambda:response.read(1024*1024),b''): h.update(part);size+=len(part)
   if size!=info['size'] or h.hexdigest()!=info['sha256']: raise RuntimeError('Deployed bytes do not match committed original: '+url)
   return {'url':url,'size':size,'sha256':h.hexdigest()}
  except Exception:
   if attempt==3: raise
   time.sleep(8)

def urls(page):
 return page.locator('a[href]').evaluate_all('(nodes)=>nodes.map(a=>({url:a.href,text:a.textContent.trim()}))')

def contains(rows,url,title=None):
 return any(x['url']==url and (title is None or x['text']==title) for x in rows)

def retry_page(page,url,check):
 last=None
 for attempt in range(8):
  try:
   response=page.goto(url,wait_until='domcontentloaded',timeout=45000)
   if response is None or response.status!=200: raise RuntimeError('Page did not return HTTP 200: '+url)
   page.wait_for_timeout(2000)
   check(page);return
  except Exception as error:
   last=error
   if attempt!=7: time.sleep(10)
 raise last

def run(phase):
 plan=load_plan()
 if not plan['records']: raise RuntimeError('No records: no completion proof is issued')
 if phase=='final': read_proof('index-sync.json',plan);read_proof('live.json',plan)
 report={**proof_base(plan),'passed':False,'phase':phase,'checks':[],'slugs':[],'errors':[]}
 filename='final.json' if phase=='final' else 'live.json'
 try:
  checks=[]
  for task in plan['records']:
   for info in task['files']:
    checks.append((task['metadata']['url']+quote(info['path'],safe='/'),info))
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   report['originalFiles']=list(pool.map(download_check,checks))
  with sync_playwright() as p:
   browser=p.chromium.launch()
   context=browser.new_context(viewport={'width':1365,'height':900},service_workers='block')
   page=context.new_page()
   for task in plan['records']:
    m=task['metadata']
    api('repos/softm/hwagok-farm/contents/'+m['recordPath']+'?ref='+plan['sourceSha'],os.getenv('GH_TOKEN',''))
    def detail(page):
     heading=page.locator('h1').first.inner_text().strip()
     if heading!=m['title']: raise RuntimeError('Canonical title mismatch: '+m['slug'])
    retry_page(page,m['url'],detail)
    page.locator('img').evaluate_all("nodes=>nodes.forEach(img=>{img.loading='eager';img.scrollIntoView()})")
    image_results=page.locator('img').evaluate_all("""async nodes=>Promise.all(nodes.map(async img=>{
      try { await Promise.race([img.decode(),new Promise((_,reject)=>setTimeout(()=>reject(Error('image timeout')),20000))]); }
      catch(e) { return {src:img.currentSrc||img.src,ok:false,error:String(e)}; }
      return {src:img.currentSrc||img.src,ok:img.naturalWidth>0};
    }))""")
    if any(not x['ok'] for x in image_results): raise RuntimeError('Broken image: '+m['slug']+' '+json.dumps(image_results,ensure_ascii=False))
    media_results=[]
    for media in page.locator('video,audio').all():
     media.scroll_into_view_if_needed()
     result=media.evaluate("""async el=>{
       el.muted=true;el.preload='auto';el.load();
       try {
         await Promise.race([new Promise((ok,bad)=>{if(el.readyState>=2)ok();else{el.addEventListener('loadeddata',ok,{once:true});el.addEventListener('error',bad,{once:true})}}),new Promise((_,bad)=>setTimeout(()=>bad(Error('metadata timeout')),30000))]);
         await el.play();await new Promise(ok=>setTimeout(ok,1800));
         const time=el.currentTime;el.pause();return {src:el.currentSrc,ok:time>0,time,duration:el.duration};
       }catch(e){return {src:el.currentSrc,ok:false,error:String(e)}}
     }""")
     media_results.append(result)
    if any(not x['ok'] for x in media_results): raise RuntimeError('Media playback failed: '+m['slug']+' '+json.dumps(media_results,ensure_ascii=False))
    report.setdefault('renderedRecords',[]).append({'slug':m['slug'],'heading':m['title'],'images':image_results,'media':media_results})
    report['slugs'].append(m['slug'])
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(RUN/('mobile-'+hashlib.sha256(m['slug'].encode()).hexdigest()[:12]+'.png')),full_page=False)
    page.set_viewport_size({'width':1365,'height':900})
   def service(page):
    links=urls(page)
    for task in plan['records']:
     m=task['metadata']
     if not contains(links,m['url'],m['title']) or not contains(links,m['repoUrl']): raise RuntimeError('Service title/detail/source directory link missing: '+m['slug'])
   retry_page(page,HOME,service)
   report['checks']=['detail','service-home','media','original-bytes','source-directory-links','title-parity']
   if phase=='final':
    def central(page):
     links=urls(page)
     for task in plan['records']:
      m=task['metadata']
      if not contains(links,m['url'],m['title']) or not contains(links,m['repoUrl']): raise RuntimeError('Central home not rendered with canonical record/source links: '+m['slug'])
    retry_page(page,CENTRAL,central)
    page.screenshot(path=str(RUN/'central-home.png'),full_page=True)
    def top(page):
     if not page.locator('#results').count(): raise RuntimeError('Top index record area missing')
     rows=page.locator('#results a[href]').evaluate_all('(nodes)=>nodes.map(a=>({url:a.href,text:a.textContent.trim()}))')
     if not contains(rows,CENTRAL): raise RuntimeError('Top index does not render the project home link')
     card=page.locator('[data-record="'+CENTRAL+'"]')
     count=read_proof('index-sync.json',plan)['publicCount']
     if not card.count() or ('공개 '+str(count)) not in card.first.inner_text(): raise RuntimeError('Top index record count is stale')
    retry_page(page,'https://softm.github.io/projects/',top)
    page.screenshot(path=str(RUN/'top-projects.png'),full_page=True)
    report['checks']+=['central-home','top-index']
   browser.close()
  report['passed']=True
 except Exception as error:
  report['errors'].append(str(error))
 finally:
  jwrite(RUN/filename,report)
 if not report['passed']: raise SystemExit('Live verification failed; inbox retained. See '+str(RUN/filename))
 print(json.dumps({'phase':phase,'passed':True,'records':len(report['slugs']),'originalFiles':len(report['originalFiles'])}))

if __name__=='__main__':
 phase=sys.argv[1] if len(sys.argv)==2 else ''
 if phase not in {'live','final'}: raise SystemExit('live | final')
 run(phase)
