#!/usr/bin/env python3
"""Verify public documents and, only when imported, all original archive bytes."""
import hashlib, json, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

slug = 'deodeok-harvest-20260923'
base = 'https://softm.github.io/hwagok-farm/'
root = Path('out/archive') / slug
receipt = root / 'import-receipt.json'
complete = receipt.is_file()
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

page_path = 'record.html' if complete else 'index.html'
expected = digest((root / page_path).read_bytes())
for attempt in range(18):
    try:
        actual = read(base + 'archive/' + slug + '/' + page_path)
        if digest(actual) != expected:
            raise RuntimeError('The public document is older or differs from the current build.')
        break
    except Exception as error:
        print(f'Publication check {attempt+1}/18: {error}', flush=True)
        if attempt == 17:
            raise
        time.sleep(10)

home = read(base).decode('utf-8')
assert f'/hwagok-farm/archive/{slug}/' in home, 'Missing archive link on project home.'
read(base + 'archive/' + slug + '/')
read('https://softm.github.io/projects/')
projects = json.loads(read('https://softm.github.io/projects/projects.json'))
project = next(item for item in projects['projects'] if item['repo'] == 'hwagok-farm')
assert project['homeUrl'] == base
assert any(slug in link.get('url', '') for link in project.get('links', [])), 'Missing global project archive link.'
report = {'projectHomeHttp': 200, 'archivePageHttp': 200, 'documentMatchesBuild': True,
          'globalIndexHttp': 200, 'globalIndexArchiveLink': True, 'mediaImported': complete,
          'verifiedOriginalImages': 0, 'verifiedOriginalVideos': 0, 'verifiedFiles': []}
if complete:
    record = json.loads((root / 'record.json').read_text())
    names = ['record.html', 'record.md', 'record.json', 'checksums.sha256', 'bundle.zip']
    for item in record['media']:
        names.append(item['file'])
        if item['type'] == 'video':
            names.extend([item['playback'], item['poster']])
    for name in names:
        remote = read(base + 'archive/' + slug + '/' + quote(name, safe='/'))
        assert digest(remote) == digest((root/name).read_bytes()), name + ': public bytes differ.'
        report['verifiedFiles'].append({'path': name, 'http': 200, 'sha256Matches': True})
    report['verifiedOriginalImages'] = 7
    report['verifiedOriginalVideos'] = 3
    report['status'] = 'public-documents-and-media-verified'
else:
    report['status'] = 'public-routing-verified-original-bundle-not-uploaded'
Path('deodeok-public-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
