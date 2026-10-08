#!/usr/bin/env python3
"""Scoped 2026-10-08 inbox batch. Preserve source bytes; never infer publication from CI."""
from __future__ import annotations
import concurrent.futures as cf
import copy, csv, datetime as dt, hashlib, html, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

BATCH='20261008-hwagok-media-inbox'
HOME='https://softm.github.io/hwagok-farm/'
CENTRAL='https://softm.github.io/projects/hwagok-farm/'
TOP='https://softm.github.io/projects/'
RUN=Path('.archive-run')/BATCH
BATCH_PATH=Path('public/archive-batches')/(BATCH+'.json')
INPUTS=[
 {'name':'20260905 무 열무 파종','tree':'7df15f1cdc6e062fcedf903723b2be293aed8351','slug':'20260905-radish-sowing'},
 {'name':'20260913 씨박 수확','tree':'35db2f5c9692897afe89af1781faad869489b237','slug':'20260913-seed-gourd-harvest'},
 {'name':'20260913 열무왕무밭 물주고 이음 재배중','tree':'94582b8d9e886d9db767f01b320742ac8fb01dee','slug':'20260913-radish-irrigation'},
 {'name':'20260913 쪽파 정식 로터리 12중 한줄 80구멍 약 1000개','tree':'c76cf36930313c1d36196d7c23ca97d74a2a1278','slug':'20260913-scallion-planting'},
]
IMAGE={'.jpg','.jpeg','.png','.webp'}
VIDEO={'.mp4','.mov','.m4v','.webm'}
IGNORE={'.DS_Store','Thumbs.db','__MACOSX','.gitkeep'}

def git(*args):
 return subprocess.check_output(['git',*args],text=True).strip()
def run(*args):
 subprocess.run(list(args),check=True)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(p,data):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def inventory(root):
 out=[]
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if any(s in IGNORE or s.startswith('._') for s in rel.parts):continue
  if p.is_symlink():raise RuntimeError('Symlink input rejected: '+str(rel))
  if p.is_file():out.append({'path':rel.as_posix(),'size':p.stat().st_size,'sha256':sha(p)})
 return out

def unchanged(root,items):
 for x in items:
  p=root/x['path']
  if not p.is_file() or p.stat().st_size!=x['size'] or sha(p)!=x['sha256']:
   raise RuntimeError('Missing or changed original: '+str(p))
def norm(s):return re.sub(r'\s+',' ',s).strip()
def http(url,timeout=90):
 if not url.startswith('https://softm.github.io/'):raise RuntimeError('Unexpected verification origin')
 with urlopen(Request(url,headers={'User-Agent':'SOFTM-Archive-Batch','Cache-Control':'no-cache'}),timeout=timeout) as r:
  if r.status!=200:raise RuntimeError('HTTP '+str(r.status))
  return r.read()
def archive_data(text):
 m=re.search(r'(<script\b[^>]*\bid=[\"\x27]archive-data[\"\x27][^>]*>)(.*?)(</script>)',text,re.S)
 if not m:raise RuntimeError('Canonical archive-data missing')
 rows=json.loads(m[2])
 if not isinstance(rows,list):raise RuntimeError('Invalid archive-data')
 return rows,m

def preview(src,dst,f):
 from PIL import Image,ImageOps
 code=f['sha256'][:20];directory=dst/'_preview';directory.mkdir(exist_ok=True)
 poster=directory/(code+'.jpg');ext=src.suffix.lower();info={**f}
 if ext in IMAGE:
  if not poster.exists():
   with Image.open(src) as im:
    im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((960,720));im.save(poster,quality=83,optimize=True)
  info.update(kind='image',preview=poster.relative_to(dst).as_posix(),playPath=f['path'])
 else:
  result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)],text=True))
  stream=next(s for s in result['streams'] if s['codec_type']=='video')
  info.update(kind='video',codec=stream.get('codec_name'),duration=float(result.get('format',{}).get('duration',0)),playPath=f['path'])
  if stream.get('codec_name') not in ('h264','vp8','vp9','av1'):
   converted=directory/(code+'.mp4')
   if not converted.exists():
    run('ffmpeg','-v','error','-y','-i',str(src),'-vf','scale=min(1280\\,iw):-2','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(converted))
   info.update(playPath=converted.relative_to(dst).as_posix(),converted=True)
  if not poster.exists():run('ffmpeg','-v','error','-y','-i',str(src),'-frames:v','1','-vf','scale=720:-2',str(poster))
  info['preview']=poster.relative_to(dst).as_posix()
 return info

CSS='''*{box-sizing:border-box}body{margin:0;background:#f4f7f4;color:#20352a;font:16px/1.65 system-ui,-apple-system,sans-serif}main,header{max-width:1180px;margin:auto;padding:22px}header{border-bottom:1px solid #d4dfd7}nav{display:flex;gap:14px;flex-wrap:wrap}a{color:#176447;overflow-wrap:anywhere}h1{font-size:clamp(22px,3vw,34px);overflow-wrap:anywhere;line-height:1.4}h2{font-size:21px}.info{width:100%;border-collapse:collapse;background:#fff}.info td,.info th{border-bottom:1px solid #d4dfd7;padding:9px;text-align:left}.note{padding:12px;background:#eaf2ec;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.item{margin:0;border:1px solid #d4dfd7;border-radius:10px;overflow:hidden;background:white}.item button{border:0;padding:0;width:100%;background:#edf1ed;cursor:zoom-in}.item img{width:100%;height:225px;object-fit:contain}.item video{width:100%;max-height:440px;background:#101b15}.item figcaption{padding:10px;overflow-wrap:anywhere;font-size:14px}small{display:block;color:#617266}.table-scroll{overflow:auto}.files{border-collapse:collapse;font-size:13px;width:100%}.files td,.files th{padding:8px;border-bottom:1px solid #d4dfd7;text-align:left}.files code{overflow-wrap:anywhere}dialog{border:0;border-radius:12px;max-width:97vw;max-height:96vh;padding:12px}dialog::backdrop{background:#07150dea}.toolbar{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.toolbar button{font:inherit;padding:6px 14px}#full{display:block;max-width:90vw;max-height:75vh;margin:auto;object-fit:contain}#caption{text-align:center;overflow-wrap:anywhere}footer{margin:30px 0}.count{font-weight:bold}@media(max-width:600px){main,header{padding:15px}.grid{grid-template-columns:1fr}.info th{min-width:90px}#full{max-width:87vw}}
'''
JS='''(()=>{const buttons=[...document.querySelectorAll('button[data-full]')],dialog=document.getElementById('lightbox'),image=document.getElementById('full'),caption=document.getElementById('caption'),original=document.getElementById('original');let at=0;function show(i){at=(i+buttons.length)%buttons.length;const b=buttons[at];image.src=b.dataset.full;image.alt=b.dataset.label;caption.textContent=(at+1)+' / '+buttons.length+' · '+b.dataset.label;original.href=b.dataset.full;if(!dialog.open)dialog.showModal()}buttons.forEach((b,i)=>b.addEventListener('click',()=>show(i)));document.getElementById('close').onclick=()=>dialog.close();document.getElementById('prev').onclick=()=>show(at-1);document.getElementById('next').onclick=()=>show(at+1);document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='ArrowRight')show(at+1);if(e.key==='ArrowLeft')show(at-1)});dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});})();'''
def shell(meta,media,original,summary_name):
 e=lambda s:html.escape(str(s),quote=True)
 q=lambda s:quote(s,safe='/')
 dates=sorted(set(x['path'][:8] for x in original if re.match(r'^20\d{6}',x['path'])))
 date_note=' · '.join(dates)
 pics=[x for x in media if x['kind']=='image'];vids=[x for x in media if x['kind']=='video']
 intro='입력 폴더에는 사진·영상 원본만 있어 원본 자료를 바로 볼 수 있는 아카이브를 구성했습니다. 작업 내용은 폴더명으로 제공된 범위를 넘겨 추정하지 않았습니다.'
 if meta['reusedCanonical']:intro+=' 같은 원본이 이미 포함된 기존 기록의 주소와 본문은 보존하고 이번 폴더의 원본 목록을 연결했습니다.'
 parts=['<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(meta['listTitle'])+'</title><style>'+CSS+'</style></head><body><header><nav><a href="'+HOME+'">화곡농장 기록</a><a href="'+CENTRAL+'">프로젝트 홈</a><a href="'+TOP+'">전체 프로젝트</a><a href="./">기록 본문</a></nav><h1>'+e(meta['listTitle'])+'</h1></header><main><p class="note">'+intro+'</p><table class="info"><tr><th>기록일</th><td>'+meta['date']+' · 입력 폴더명 기준</td></tr><tr><th>원본 자료</th><td>사진 '+str(len(pics))+'개 · 영상 '+str(len(vids))+'개 · 전체 '+str(len(original))+'개</td></tr><tr><th>파일명 날짜</th><td>'+e(date_note)+' · 폴더명과 다를 수 있으며 원본 파일명은 변경하지 않았습니다.</td></tr><tr><th>문서·목록</th><td><a href="'+q(summary_name)+'">Markdown 정리</a> · <a href="source-inventory-'+meta['inputTree'][:10]+'.csv">원본 검증 목록</a></td></tr></table>']
 for kind,label,items in [('image','사진',pics),('video','영상',vids)]:
  if not items:continue
  parts.append('<h2>'+label+' <span class="count">'+str(len(items))+'</span></h2><div class="grid">')
  for f in items:
   original_url=q(f['path']);label=e(f['path']);poster=q(f['preview'])
   if kind=='image':body='<button type="button" data-full="'+original_url+'" data-label="'+label+'" aria-label="'+label+' 확대"><img loading="lazy" src="'+poster+'" alt="'+label+'"></button>'
   else:body='<video controls playsinline preload="metadata" poster="'+poster+'" src="'+q(f['playPath'])+'" data-original="'+original_url+'"></video>'
   parts.append('<figure class="item">'+body+'<figcaption>'+label+'<small>'+format(f['size']/1048576,'.2f')+' MiB'+(' · 브라우저용 변환본 재생, 원본 별도 보존' if f.get('converted') else '')+'</small><a href="'+original_url+'" target="_blank" rel="noopener">원본 열기</a> · <a href="'+original_url+'" download>원본 저장</a></figcaption></figure>')
  parts.append('</div>')
 parts.append('<h2>원본 파일 전체 목록</h2><div class="table-scroll"><table class="files"><tr><th>파일명</th><th>크기</th><th>SHA-256</th></tr>')
 for f in original:parts.append('<tr><td><a href="'+q(f['path'])+'">'+e(f['path'])+'</a></td><td>'+str(f['size'])+'</td><td><code>'+f['sha256']+'</code></td></tr>')
 parts.append('</table></div><footer><a href="'+meta['repoUrl']+'">GitHub 원본 기록 폴더</a></footer></main><dialog id="lightbox"><div class="toolbar"><button id="prev">이전</button><button id="next">다음</button><a id="original" target="_blank" rel="noopener">원본 열기</a><button id="close">닫기</button></div><img id="full" alt="확대 원본"><p id="caption"></p></dialog><script>'+JS+'</script></body></html>')
 return ''.join(parts)

def build():
 from bs4 import BeautifulSoup
 RUN.mkdir(parents=True,exist_ok=True)
 home=Path('index.html');home_text=home.read_text(encoding='utf-8');rows,match=archive_data(home_text)
 original_rows=copy.deepcopy(rows);records=[];used=set()
 for conf in INPUTS:
  name=conf['name'];src=Path('zip')/name
  if git('rev-parse','HEAD:'+src.as_posix())!=conf['tree']:raise RuntimeError('Input changed; review required: '+name)
  source=inventory(src)
  if not source or any(Path(f['path']).suffix.lower() not in IMAGE|VIDEO for f in source):raise RuntimeError('This reviewed batch expects media-only folders: '+name)
  date=dt.datetime.strptime(name[:8],'%Y%m%d').date().isoformat();hashes={f['sha256'] for f in source}
  candidates=[]
  for mp in Path('public/records').glob('*/archive-manifest.json'):
   m=read(mp);oldmeta=m.get('metadata',m);old_date=oldmeta.get('date') or next((x.get('date') for x in rows if x.get('dir')==mp.parent.name),'')
   if old_date!=date:continue
   old_hashes={x.get('sha256') for x in m.get('files',[])}
   if hashes<=old_hashes:candidates.append(mp.parent)
  if len(candidates)>1:raise RuntimeError('Ambiguous duplicate source; retain input: '+name)
  dst=candidates[0] if candidates else Path('public/records')/conf['slug']
  slug=dst.name
  if slug in used:raise RuntimeError('Two inputs unexpectedly map to one record')
  used.add(slug);exists=dst.exists();old_files=inventory(dst) if exists else []
  if exists and not candidates:
   old=read(dst/'archive.json') if (dst/'archive.json').exists() else {}
   if old.get('inputTree')!=conf['tree']:raise RuntimeError('Existing canonical has another source')
  dst.mkdir(parents=True,exist_ok=True)
  prior_manifest=dst/'archive-manifest.json'
  history=dst/'archive-inputs'/(conf['tree']+'-previous-manifest.json')
  if prior_manifest.exists() and not history.exists():history.parent.mkdir(exist_ok=True);shutil.copy2(prior_manifest,history)
  for f in source:
   target=dst/f['path'];target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists() and sha(target)!=f['sha256']:raise RuntimeError('Original path collision: '+str(target))
   if not target.exists():shutil.copy2(src/f['path'],target)
  unchanged(dst,source)
  media=[preview(dst/f['path'],dst,f) for f in source]
  image_count=sum(f['kind']=='image' for f in media);video_count=len(media)-image_count
  oldmeta=read(dst/'archive.json') if (dst/'archive.json').exists() else {}
  existing_doc=(dst/'index.html').read_text(encoding='utf-8') if exists and (dst/'index.html').exists() else ''
  oldh1=BeautifulSoup(existing_doc,'html.parser').find('h1') if existing_doc else None
  source_title=norm(oldh1.get_text(' ',strip=True)) if oldh1 else name
  viewer='inbox-'+conf['tree'][:10]+'-viewer.html';summary='inbox-'+conf['tree'][:10]+'-summary.md'
  metadata={**oldmeta,'schemaVersion':3,'id':oldmeta.get('id',slug),'slug':slug,'directory':slug,'recordPath':dst.as_posix(),'inputName':name,'inputKind':'folder','inputTree':conf['tree'],'listTitle':name,'title':name,'label':name,'titleSource':'inbox-name','sourceTitle':source_title,'date':date,'dateSource':'archive-canonical','visibility':'public','category':'영농 기록','url':HOME+'records/'+slug+'/','repoUrl':'https://github.com/softm/hwagok-farm/tree/main/'+dst.as_posix(),'attachmentsUrl':HOME+'records/'+slug+'/'+viewer,'reusedCanonical':exists,'batch':BATCH,'media':{'images':image_count,'videos':video_count,'audio':0,'originalFiles':len(source)},'summary':'입력 폴더 원본 사진 '+str(image_count)+'개·영상 '+str(video_count)+'개. 폴더명 그대로 제목을 사용하며 원본 파일을 보존합니다.'}
  text=shell(metadata,media,source,summary);(dst/viewer).write_text(text,encoding='utf-8')
  if not existing_doc:(dst/'index.html').write_text(text,encoding='utf-8')
  md=['# '+name,'','| 항목 | 내용 |','|---|---|','| 기록일 | '+date+' · 폴더명 기준 |','| 사진 | '+str(image_count)+'개 |','| 영상 | '+str(video_count)+'개 |','','입력에는 사진·영상 원본만 있습니다. 작업 내용은 폴더명으로 제공된 범위를 넘겨 추정하지 않았습니다.','파일명 날짜가 폴더 날짜와 달라도 원본 파일명과 목록 제목은 유지합니다.','','[원본 미디어 보기]('+viewer+')','','## 원본 목록','']
  for f in source:md.append('- ['+f['path']+']('+quote(f['path'],safe='/')+') · '+str(f['size'])+' bytes · SHA-256 `'+f['sha256']+'`')
  (dst/summary).write_text('\n'.join(md)+'\n',encoding='utf-8')
  csvpath=dst/('source-inventory-'+conf['tree'][:10]+'.csv')
  with csvpath.open('w',encoding='utf-8-sig',newline='') as output:
   w=csv.DictWriter(output,fieldnames=['path','size','sha256']);w.writeheader();w.writerows(source)
  write(dst/'archive.json',metadata)
  write(dst/'archive-inputs'/(conf['tree']+'.json'),{'inputName':name,'inputTree':conf['tree'],'inputKind':'folder','files':source,'metadata':metadata})
  protected=[f for f in old_files if f['path'] not in ('archive.json','archive-manifest.json') and not f['path'].startswith(('_preview/','archive-inputs/','inbox-','source-inventory-'))]
  unchanged(dst,protected)
  all_files=[f for f in inventory(dst) if f['path']!='archive-manifest.json']
  write(prior_manifest,{'schemaVersion':3,'metadata':metadata,'inputName':name,'inputTree':conf['tree'],'source':name,'files':all_files,'originals':source,'originalFileCount':len(source),'preservedExistingFiles':len(protected)})
  row={'date':date,'kind':metadata['category'],'title':name,'dir':slug,'desc':metadata['summary'],'url':metadata['url'],'repoUrl':metadata['repoUrl'],'attachmentsUrl':metadata['attachmentsUrl'],'inputName':name,'inputKind':'folder','listTitle':name,'titleSource':'inbox-name','sourceTitle':source_title}
  rows=[x for x in rows if x.get('dir')!=slug];rows.append(row)
  generated_paths={'index.html',viewer,summary,'archive.json','archive-manifest.json',csvpath.name}
  checks=source+[f for f in inventory(dst) if f['path'] in generated_paths or f['path'].startswith('_preview/')]
  records.append({'input':src.as_posix(),'inputTree':conf['tree'],'metadata':metadata,'originals':source,'files':checks,'media':media,'protectedExisting':protected,'manifestSha256':sha(prior_manifest)})
  print(json.dumps({'title':name,'slug':slug,'images':image_count,'videos':video_count,'originalFiles':len(source),'reused':exists},ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:(x.get('date',''),x.get('title','')),reverse=True)
 for old in original_rows:
  if old.get('dir') not in used and old not in rows:raise RuntimeError('Unrelated catalogue row changed')
 payload=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 home_text=home_text[:match.start(2)]+payload+home_text[match.end(2):]
 links='<section id="'+BATCH+'"><h2>새 입력 자료 · 원본 보기</h2>'+''.join('<p><a href="'+r['metadata']['attachmentsUrl']+'">'+html.escape(r['metadata']['listTitle'])+' · 사진·영상</a></p>' for r in records)+'</section>'
 home_text=re.sub(r'<section id="'+BATCH+r'">.*?</section>','',home_text,flags=re.S)
 home_text=home_text.replace('</main>',links+'</main>',1);home.write_text(home_text,encoding='utf-8')
 plan={'batch':BATCH,'records':records,'publicCount':len(rows),'newRecords':sum(not r['metadata']['reusedCanonical'] for r in records),'reusedRecords':sum(r['metadata']['reusedCanonical'] for r in records)}
 write(RUN/'plan.json',plan);write(BATCH_PATH,{'batch':BATCH,'publicCount':len(rows),'newRecords':plan['newRecords'],'reusedRecords':plan['reusedRecords'],'records':[r['metadata'] for r in records]})
 print(json.dumps({'batch':BATCH,'publicCount':len(rows),'new':plan['newRecords'],'reused':plan['reusedRecords']},ensure_ascii=False),flush=True)

def stamp():
 plan=read(RUN/'plan.json');plan['sourceCommit']=git('rev-parse','HEAD');write(RUN/'plan.json',plan)
def proofbase(plan):return {'sourceCommit':plan['sourceCommit'],'planHash':sha(RUN/'plan.json'),'batch':BATCH}
def downloaded(task):
 url,f=task
 for attempt in range(4):
  try:
   data=http(url+quote(f['path'],safe='/')+'?verify='+BATCH,120)
   if len(data)!=f['size'] or hashlib.sha256(data).hexdigest()!=f['sha256']:raise RuntimeError('Deployed original differs: '+url+f['path'])
   return {'url':url+quote(f['path'],safe='/'),'size':f['size'],'sha256':f['sha256'],'status':200}
  except Exception:
   if attempt==3:raise
   time.sleep(12)

def verify(phase):
 from playwright.sync_api import sync_playwright
 plan=read(RUN/'plan.json');final=phase=='final';report={**proofbase(plan),'passed':False,'phase':phase,'records':[]}
 try:
  if final:
   earlier=read(RUN/'live.json')
   if not earlier.get('passed') or any(earlier.get(k)!=v for k,v in proofbase(plan).items()):raise RuntimeError('Live verification missing/stale')
  with cf.ThreadPoolExecutor(max_workers=4) as pool:
   report['fileChecks']=list(pool.map(downloaded,[(r['metadata']['url'],f) for r in plan['records'] for f in (r['originals'] if final else r['files'])]))
  with sync_playwright() as pw:
   browser=pw.chromium.launch(channel='chrome',args=['--autoplay-policy=no-user-gesture-required'])
   context=browser.new_context(viewport={'width':1365,'height':900},service_workers='block');page=context.new_page()
   def visit(url):
    res=page.goto(url,wait_until='domcontentloaded',timeout=60000)
    if not res or res.status!=200:raise RuntimeError('Page HTTP error '+url)
   for r in plan['records']:
    m=r['metadata'];visit(m['url']);page.locator('h1').first.wait_for()
    if norm(page.locator('h1').first.inner_text())!=m['sourceTitle']:raise RuntimeError('Original heading changed: '+m['slug'])
    visit(m['attachmentsUrl']);page.locator('h1').first.wait_for()
    if page.locator('h1').first.inner_text()!=m['listTitle']:raise RuntimeError('Viewer title differs')
    image_results=page.locator('img[src]').evaluate_all("""async ns=>{ns.forEach(n=>n.loading='eager');return await Promise.all(ns.map(async n=>{try{await Promise.race([n.decode(),new Promise((_,bad)=>setTimeout(()=>bad(Error('timeout')),45000))]);return {src:n.currentSrc,ok:n.naturalWidth>0}}catch(e){return {src:n.src,ok:false,error:String(e)}}}))}""")
    if len(image_results)!=m['media']['images'] or any(not x['ok'] for x in image_results):raise RuntimeError('Image rendering failed: '+m['slug'])
    first=page.locator('button[data-full]').first;first.click();dialog=page.locator('dialog[open]');dialog.wait_for(state='visible')
    dialog.locator('#full').evaluate('async n=>{await n.decode();if(!n.naturalWidth)throw Error("Missing full image")}')
    if m['media']['images']>1:
     dialog.locator('#next').click();dialog.locator('#full').evaluate('async n=>{await n.decode();if(!n.naturalWidth)throw Error("Missing next image")}')
    dialog.locator('#close').click();dialog.wait_for(state='hidden')
    videos=[]
    for v in page.locator('video').all():
     v.scroll_into_view_if_needed()
     result=v.evaluate("""async el=>{el.muted=true;try{await Promise.race([el.play(),new Promise((_,bad)=>setTimeout(()=>bad(Error('play timeout')),45000))]);await new Promise(ok=>setTimeout(ok,1200));const frames=el.getVideoPlaybackQuality().totalVideoFrames;const out={src:el.currentSrc,time:el.currentTime,frames,ok:el.currentTime>0&&frames>0};el.pause();return out}catch(e){el.pause();return {src:el.currentSrc,ok:false,error:String(e)}}}""")
     videos.append(result)
     if not result['ok']:raise RuntimeError('Video playback failed: '+json.dumps(result))
    if len(videos)!=m['media']['videos']:raise RuntimeError('Missing video controls')
    page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(RUN/(m['slug']+'-desktop.png')))
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(RUN/(m['slug']+'-mobile.png')))
    if page.evaluate('document.documentElement.scrollWidth>window.innerWidth+3'):raise RuntimeError('Mobile page horizontal overflow')
    page.set_viewport_size({'width':1365,'height':900})
    report['records'].append({'title':m['listTitle'],'url':m['url'],'attachmentsUrl':m['attachmentsUrl'],'images':len(image_results),'videos':len(videos),'playback':videos,'zoom':True,'mobile':True,'originalHeadingPreserved':True,'reusedCanonical':m['reusedCanonical']})
   visit(HOME)
   for r in plan['records']:
    m=r['metadata'];link=page.locator('a.record-title').filter(has_text=m['listTitle']);link.first.wait_for(state='visible',timeout=45000)
    if link.count()!=1 or link.first.inner_text()!=m['listTitle'] or link.first.get_attribute('href')!=m['url']:raise RuntimeError('Service title/URL mismatch')
    if not page.locator('a[href="'+m['repoUrl']+'"]').count():raise RuntimeError('Service original-directory link missing')
   report['serviceHome']=True
   if final:
    def central_links():
     visit(CENTRAL)
     for r in plan['records']:
      m=r['metadata'];a=page.locator('a[href="'+m['url']+'"]').filter(has_text=m['listTitle']);a.first.wait_for(state='visible',timeout=45000)
      if a.first.inner_text()!=m['listTitle']:raise RuntimeError('Central title mismatch')
      if not page.locator('a[href="'+m['repoUrl']+'"]').count():raise RuntimeError('Central source-directory link missing')
    central_links();page.screenshot(path=str(RUN/'central-project-home.png'),full_page=True)
    for r in plan['records']:
     m=r['metadata'];page.locator('a[href="'+m['url']+'"]').filter(has_text=m['listTitle']).first.click();page.wait_for_url(m['url'],timeout=45000)
     if norm(page.locator('h1').first.inner_text())!=m['sourceTitle']:raise RuntimeError('Deep link led to wrong body')
     central_links()
    data=json.loads(http(TOP+'projects.json?verify='+str(time.time_ns())));p=next(x for x in data['projects'] if x['repo']=='hwagok-farm')
    for r in plan['records']:
     x=next(x for x in p['links'] if x['url']==r['metadata']['url'])
     if x.get('listTitle',x['title'])!=r['metadata']['listTitle']:raise RuntimeError('Central JSON title stale')
    public=sum(x.get('visibility')=='public' for x in p['links']);private=sum(x.get('visibility')=='private' for x in p['links'])
    if public!=plan['publicCount']:raise RuntimeError('Central count mismatch')
    visit(TOP);card=page.locator('[data-record="'+CENTRAL+'"]');card.first.wait_for(state='visible',timeout=45000)
    if '공개 '+str(public) not in card.inner_text() or '비공개 '+str(private) not in card.inner_text():raise RuntimeError('Top project counts stale')
    page.screenshot(path=str(RUN/'top-projects.png'),full_page=True)
    card.locator('a[href="'+CENTRAL+'"]').first.click();page.wait_for_url(CENTRAL,timeout=45000)
    report.update(centralHome=True,topProjects=True,deepLinks=True,publicCount=public,privateCount=private,totalCount=public+private)
   browser.close()
  report['passed']=True;report['verifiedAt']=dt.datetime.now(dt.timezone.utc).isoformat()
 except Exception as e:
  report['error']=str(e);raise
 finally:write(RUN/(phase+'.json'),report)
 print(json.dumps({k:v for k,v in report.items() if k not in ('fileChecks','records')},ensure_ascii=False),flush=True)

def cleanup():
 plan=read(RUN/'plan.json');proof=read(RUN/'final.json')
 if not all(proof.get(k) is True for k in ['passed','serviceHome','centralHome','topProjects','deepLinks']):raise RuntimeError('Incomplete final verification')
 if any(proof.get(k)!=v for k,v in proofbase(plan).items()):raise RuntimeError('Stale completion evidence')
 run('git','fetch','origin','main')
 if git('rev-parse','HEAD')!=git('rev-parse','origin/main'):raise RuntimeError('Concurrent source update; preserve inbox')
 for r in plan['records']:
  if git('rev-parse','HEAD:'+r['input'])!=r['inputTree']:raise RuntimeError('Input changed; preserve inbox')
  dst=Path(r['metadata']['recordPath']);unchanged(dst,r['originals']);unchanged(dst,r['protectedExisting'])
  if sha(dst/'archive-manifest.json')!=r['manifestSha256']:raise RuntimeError('Manifest changed')
 receipt={**proof,'inputCleanup':'only these verified unchanged folders; originals retained','inputs':[{'path':r['input'],'tree':r['inputTree'],'recordPath':r['metadata']['recordPath']} for r in plan['records']]}
 report=Path('reports')/(BATCH+'-completion.json');write(report,receipt)
 run('git','rm','-r','--',*[r['input'] for r in plan['records']]);run('git','add','--',str(report))
 run('git','commit','-m','archive: clean four verified inbox inputs; retain every original and completion evidence')
 run('git','push','origin','HEAD:main')

def catalog():
 # Executed in central repository. Public metadata only; no private origin fetches.
 expected_names={x['name'] for x in INPUTS}
 for attempt in range(100):
  try:
   batch=json.loads(http(HOME+'archive-batches/'+BATCH+'.json?sync='+str(time.time_ns())))
   if batch['batch']!=BATCH or {r['inputName'] for r in batch['records']}!=expected_names:raise RuntimeError('Unexpected deployed batch')
   break
  except Exception:
   if attempt==99:raise
   time.sleep(12)
 run('git','pull','--ff-only','origin','main')
 path=Path('projects/projects.json');data=read(path);before=copy.deepcopy(data['projects']);p=next(x for x in data['projects'] if x['repo']=='hwagok-farm')
 old=copy.deepcopy(p['links']);rows,_=archive_data(http(HOME+'?sync='+str(time.time_ns())).decode('utf-8'))
 js="const fs=require('fs'),m=require('./projects/archive-sync.js');const d=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(m.archiveRows(d.rows,d.project)));"
 links=json.loads(subprocess.run(['node','-e',js],input=json.dumps({'rows':rows,'project':p},ensure_ascii=False),text=True,capture_output=True,check=True).stdout)
 targets={r['url']:r for r in batch['records']};old_by={x['url']:x for x in old};new=[]
 for row in links:
  if row['url'] in targets:
   m=targets[row['url']]
   if row['title']!=m['inputName']:raise RuntimeError('Input title differs in deployed service')
   new.append({**old_by.get(row['url'],{}),**row,'attachmentsUrl':m['attachmentsUrl'],'inputName':m['inputName'],'inputKind':'folder','listTitle':m['listTitle'],'titleSource':'inbox-name','sourceTitle':m['sourceTitle']})
  else:new.append(old_by.get(row['url'],row))
 old_private=[x for x in old if x.get('visibility')=='private'];p['links']=new+old_private
 for x in old:
  if x['url'] not in targets and x not in p['links']:raise RuntimeError('Unrelated record would change')
 p['homePublicListCount']=p['pageCount']=len(new);p['homePrivateListCount']=p['privatePageCount']=len(old_private);p['totalRecordCount']=len(p['links'])
 p['publicIndexSnapshot']={'source':HOME,'recordCount':len(new),'purpose':'verified public input-folder batch; private metadata preserved'}
 p['lastArchiveBatch']=BATCH
 for a,b in zip(before,data['projects']):
  if a['repo']!='hwagok-farm' and a!=b:raise RuntimeError('Unrelated project changed')
 data['updatedAt']='2026-10-08';write(path,data)
 print(json.dumps({'batch':BATCH,'inputFolders':4,'public':len(new),'private':len(old_private),'total':len(p['links']),'titles':[r['listTitle'] for r in batch['records']]},ensure_ascii=False),flush=True)

if __name__=='__main__':
 command=sys.argv[1] if len(sys.argv)==2 else ''
 if command=='build':build()
 elif command=='stamp':stamp()
 elif command in ('live','final'):verify(command)
 elif command=='cleanup':cleanup()
 elif command=='catalog':catalog()
 else:raise SystemExit('build | stamp | live | final | cleanup | catalog')
