#!/usr/bin/env python3
"""Fail a build rather than publish divergent list/detail titles. No third-party dependencies."""
import json
from html.parser import HTMLParser
from pathlib import Path

class Titles(HTMLParser):
    def __init__(self):
        super().__init__(); self.values=[]; self.active=False; self.current=[]; self.refresh=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1': self.active=True; self.current=[]
        if tag=='meta' and attrs.get('http-equiv','').lower()=='refresh': self.refresh=attrs.get('content','')
    def handle_endtag(self,tag):
        if tag=='h1' and self.active: self.active=False; self.values.append(' '.join(''.join(self.current).split()))
    def handle_data(self,data):
        if self.active:self.current.append(data)

out=Path('out'); report=json.loads((out/'detail-ui-report.json').read_text())
assert report['mediaUnchanged'], 'Binary media changed during layout normalization'
assert (out/'archive-detail.css').is_file()
assert (out/'archive-detail.js').is_file()
results=[]
for r in report['records']:
    route=r['legacyPath'].split('?')[0].lstrip('/')
    file=out/route if route.endswith('.html') else out/route/'index.html'
    assert file.is_file(),f'Missing detail route: {file}'
    text=file.read_text(); p=Titles(); p.feed(text)
    if p.refresh:
        results.append({'slug':r['slug'],'title':r['title'],'route':r['legacyPath'],'redirect':True}); continue
    assert len(p.values)==1,(str(file),p.values)
    assert p.values[0]==r['title'],(str(file),p.values[0],r['title'])
    assert 'record-date' in text, f'Missing separately styled authored date: {file}'
    results.append({'slug':r['slug'],'title':p.values[0],'route':r['legacyPath'],'matched':True})
assert results,'No detail pages checked'
report['staticVerification']={'checked':len(results),'matched':sum(bool(x.get('matched')) for x in results),'redirects':sum(bool(x.get('redirect')) for x in results),'results':results}
(out/'detail-ui-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['staticVerification'],ensure_ascii=False,indent=2))
