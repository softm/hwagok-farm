#!/usr/bin/env python3
"""Read-only production checks: canonical titles, compact layout and original fan images."""
import json, time, urllib.request
from pathlib import Path
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
    else:raise AssertionError('New production title/layout report was not published')
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
        anchor=page.locator('a[href*="fan-gearbox-repair-20260914"]').first
        card=anchor.locator('xpath=ancestor::article[1]')
        list_title=clean(card.locator('h3').inner_text())
        assert list_title==fan['title'],(list_title,fan['title'])
        result['listAndDetailTitle']=list_title
        browser.close()
    result['success']=True
except Exception as e:
    result['success']=False;result['errors'].append(str(e));raise
finally:
    (ART/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
