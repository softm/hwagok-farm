#!/usr/bin/env python3
"""Read-only production verification of titles, media and responsive layout."""
import json, time, urllib.request
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
BASE='https://softm.github.io/hwagok-farm'
ART=Path('detail-ui-verification'); ART.mkdir(exist_ok=True)
result={'base':BASE,'pages':[],'errors':[]}
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'archive-detail-verifier','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=30) as response:return response.read().decode()
def clean(value):return ' '.join(value.split())
try:
    for attempt in range(24):
        try:
            report=json.loads(get(BASE+'/detail-ui-report.json?check='+str(int(time.time()))))
            if report.get('version')=='20260930-compact-detail-v1' and report.get('staticVerification'):break
        except Exception:pass
        time.sleep(10)
    else:raise AssertionError('Current production title report not published')
    result['staticVerification']=report['staticVerification']
    result['mediaUnchanged']=report['mediaUnchanged']
    records=report['records']
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        for record in records:
            url=BASE+record['legacyPath']
            response=page.goto(url,wait_until='domcontentloaded',timeout=60000)
            page.wait_for_selector('h1');page.wait_for_timeout(250)
            actual=clean(page.locator('h1').first.inner_text())
            matched=actual==record['title']
            result['pages'].append({'slug':record['slug'],'url':url,'http':response.status if response else None,'title':actual,'expected':record['title'],'matched':matched})
            assert matched,(url,actual,record['title'])
        fan=next(r for r in records if r['slug']=='fan-gearbox-repair-20260914')
        result['responsive']=[]
        for width in [1440,768,390,320]:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto(BASE+fan['legacyPath'],wait_until='networkidle')
            page.wait_for_selector('img[data-record-zoom]')
            page.locator('.record-gallery').scroll_into_view_if_needed()
            decoded=page.evaluate('''async()=>{const images=[...document.querySelectorAll('.record-gallery img')];for(const i of images)i.loading='eager';await Promise.all(images.map(i=>i.decode().catch(()=>null)));return images.map(i=>({src:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight}));}''')
            assert len(decoded)==8 and all(i['width']>0 for i in decoded),decoded
            m=page.evaluate('''()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headerHeight:document.querySelector('header').getBoundingClientRect().height,fontSize:getComputedStyle(document.querySelector('h1')).fontSize,columns:getComputedStyle(document.querySelector('.record-gallery')).gridTemplateColumns})''')
            assert m['scrollWidth']<=width+1,m
            assert float(m['fontSize'].replace('px',''))<=34,m
            photo=page.locator('img[data-record-zoom]').first
            photo.focus();page.keyboard.press('Enter');assert page.locator('dialog').is_visible()
            page.keyboard.press('ArrowRight');assert page.locator('[data-counter]').inner_text()=='2 / 8'
            page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
            page.locator('h1').click();page.evaluate('scrollTo(0,0)')
            page.screenshot(path=str(ART/f'fan-{width}.png'),full_page=True)
            m['decodedImages']=len(decoded);result['responsive'].append(m)
        page.goto('https://softm.github.io/projects/hwagok-farm/',wait_until='networkidle')
        page.wait_for_selector('article.record-card.public')
        items=page.locator('article.record-card.public').evaluate_all('''rows=>rows.map(r=>({url:r.dataset.record,date:r.dataset.authoredDate||'',name:r.querySelector('h3').innerText}))''')
        comparisons=[]
        for item in items:
            parts=urlsplit(item['url']).path.rstrip('/').split('/')
            slug=parts[-2] if parts[-1]=='record.html' else parts[-1]
            record=next((r for r in records if r['slug']==slug),None)
            assert record is not None,('Unmapped public list record',slug)
            full=(item['date'] or '작성일 미확인')+' '+clean(item['name'])
            comparisons.append({'slug':slug,'listDate':item['date'],'listName':clean(item['name']),'detailTitle':record['title'],'matched':full==record['title']})
        result['listAndDetailTitles']=comparisons
        assert len(comparisons)==23 and all(x['matched'] for x in comparisons),comparisons
        page.set_viewport_size({'width':1440,'height':1000})
        page.screenshot(path=str(ART/'farm-list-titles.png'),full_page=True)
        deodeok=next(r for r in records if r['slug']=='deodeok-harvest-20260923')
        full_url=BASE+'/archive/deodeok-harvest-20260923/record.html'
        page.goto(full_url,wait_until='networkidle')
        assert clean(page.locator('h1').first.inner_text())==deodeok['title']
        images=page.evaluate('''async()=>{const images=[...document.querySelectorAll('img[src*="images/"]')];images.forEach(i=>i.loading='eager');await Promise.all(images.map(i=>i.decode()));return [...new Map(images.map(i=>[i.currentSrc,{src:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight}])).values()]}''')
        assert len(images)==7 and all(i['width']>0 for i in images),images
        assert page.locator('video').count()==3
        playback=[]
        for index in range(3):
            video=page.locator('video').nth(index)
            video.scroll_into_view_if_needed()
            video.evaluate('(v)=>{v.muted=true;return v.play()}')
            page.wait_for_function('(i)=>document.querySelectorAll("video")[i].currentTime>0.15',arg=index,timeout=15000)
            playback.append(video.evaluate('(v)=>({src:v.currentSrc,currentTime:v.currentTime,duration:v.duration,error:v.error?.code||null})'))
            video.evaluate('(v)=>v.pause()')
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(ART/'deodeok-title-and-media.png'),full_page=True)
        result['deodeokMedia']={'url':full_url,'title':deodeok['title'],'decodedOriginalImages':len(images),'playedVideos':len(playback),'videos':playback}
        browser.close()
    result['success']=True
except Exception as e:
    result['success']=False;result['errors'].append(str(e));raise
finally:
    (ART/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
