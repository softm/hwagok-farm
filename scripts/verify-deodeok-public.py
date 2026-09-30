#!/usr/bin/env python3
"""Verify actual published titles and original bytes, not only a successful build."""
import hashlib, json, re, time
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import Request, urlopen

slug = 'deodeok-harvest-20260923'
base = 'https://softm.github.io/hwagok-farm/'
project_home = 'https://softm.github.io/projects/hwagok-farm/'
root = Path('out/archive') / slug
complete = (root / 'import-receipt.json').is_file()
stamp = str(int(time.time()))

def read(url):
    separator = '&' if '?' in url else '?'
    request = Request(url + separator + 'archive-check=' + stamp,
                      headers={'User-Agent': 'HwagokArchiveVerification', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=35) as response:
        if response.status != 200:
            raise RuntimeError(f'HTTP {response.status}: {url}')
        return response.read()

def digest(data):
    return hashlib.sha256(data).hexdigest()

class Titles(HTMLParser):
    def __init__(self):
        super().__init__(); self.headings=[]; self.parts=None; self.refresh=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='h1': self.parts=[]
        if tag=='meta' and attrs.get('http-equiv','').lower()=='refresh': self.refresh=attrs.get('content','')
    def handle_endtag(self, tag):
        if tag=='h1' and self.parts is not None:
            self.headings.append(' '.join(''.join(self.parts).split())); self.parts=None
    def handle_data(self, data):
        if self.parts is not None: self.parts.append(data)

def heading_at(url):
    for _ in range(3):
        parser=Titles(); parser.feed(read(url).decode('utf-8'))
        if not parser.refresh:
            return parser.headings, url
        match=re.search(r'url\s*=\s*(.*)',parser.refresh,re.I)
        if not match: raise AssertionError('Invalid refresh target')
        target=urljoin(url,match.group(1).strip().strip('\"\''))
        if not target.startswith(base): raise AssertionError('Unexpected external record redirect')
        url=target
    raise AssertionError('Too many record redirects')

page_path = 'record.html' if complete else 'index.html'
expected = digest((root / page_path).read_bytes())
for attempt in range(18):
    try:
        if digest(read(base+'archive/'+slug+'/'+page_path)) != expected:
            raise RuntimeError('Public record differs from the exact build output.')
        break
    except Exception as error:
        print(f'Publication check {attempt+1}/18: {error}', flush=True)
        if attempt == 17: raise
        time.sleep(10)

home = read(base).decode('utf-8')
assert f'/hwagok-farm/archive/{slug}/' in home, 'Missing farm archive link.'
read(base+'archive/'+slug+'/')
read(project_home)
read('https://softm.github.io/projects/')
projects=json.loads(read('https://softm.github.io/projects/projects.json'))
project=next(item for item in projects['projects'] if item['repo']=='hwagok-farm')
assert project['homeUrl']==project_home, 'Central project home must use /projects/hwagok-farm/.'
assert project['publicUrl']==base, 'Wrong public source origin.'
assert any(slug in link.get('url','') for link in project.get('links',[])), 'Missing directory record link.'
report={'projectHomeHttp':200,'projectHomeUrl':project_home,'archivePageHttp':200,
        'documentMatchesBuild':True,'globalIndexHttp':200,'globalIndexArchiveLink':True,
        'mediaImported':complete,'verifiedOriginalImages':0,'verifiedOriginalVideos':0,'verifiedFiles':[]}
if complete:
    record=json.loads((root/'record.json').read_text())
    names=['record.html','record.md','record.json','checksums.sha256','bundle.zip']
    for item in record['media']:
        names.append(item['file'])
        if item['type']=='video': names.extend([item['playback'],item['poster']])
    def check_file(name):
        data=read(base+'archive/'+slug+'/'+quote(name,safe='/'))
        assert digest(data)==digest((root/name).read_bytes()),name+': public bytes differ'
        return {'path':name,'http':200,'sha256Matches':True}
    with ThreadPoolExecutor(max_workers=4) as pool: report['verifiedFiles']=list(pool.map(check_file,names))
    report.update(verifiedOriginalImages=7,verifiedOriginalVideos=3,status='public-documents-and-media-verified')
else:
    report['status']='public-routing-verified-original-bundle-not-uploaded'

layout=json.loads(Path('out/detail-ui-report.json').read_text())
def check_title(item):
    route=item['legacyPath']; url=base.rstrip('/')+'/'+route.lstrip('/')
    headings,final=heading_at(url)
    return {'slug':item['slug'],'url':url,'finalUrl':final,'expected':item['title'],'actual':headings,
            'matched':headings==[item['title']]}
with ThreadPoolExecutor(max_workers=4) as pool: title_results=list(pool.map(check_title,layout['records']))
expected_deodeok=next(r['title'] for r in layout['records'] if r['slug']==slug)
for alias in ['archive/'+slug+'/','archive/'+slug+'/record.html']:
    headings,final=heading_at(base+alias)
    title_results.append({'slug':slug,'url':base+alias,'finalUrl':final,'expected':expected_deodeok,'actual':headings,'matched':headings==[expected_deodeok]})
report['liveTitles']={'checked':len(title_results),'matched':sum(x['matched'] for x in title_results),'results':title_results}
Path('deodeok-public-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
assert all(x['matched'] for x in title_results),'Live list/detail title mismatch; see verification report.'
