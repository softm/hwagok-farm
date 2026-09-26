#!/usr/bin/env python3
"""Request actual Pages publication while preserving existing site settings."""
import json, os, time
from urllib.request import Request, urlopen

repo = os.environ['GITHUB_REPOSITORY']
if repo != 'softm/hwagok-farm':
    raise SystemExit('Unexpected repository; refusing Pages operation.')
base = 'https://api.github.com/repos/' + repo
headers = {'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'],
           'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2026-03-10'}
def api(path, method='GET'):
    request = Request(base + path, method=method, headers=headers,
                      data=b'' if method == 'POST' else None)
    with urlopen(request, timeout=30) as response:
        return json.load(response)
site = api('/pages')
mode = site.get('build_type', 'legacy')
source = site.get('source', {})
print(json.dumps({'pagesBuildType': mode, 'source': source, 'publicUrl': site.get('html_url')}, ensure_ascii=False))
with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
    output.write('build_type=' + mode + '\n')
if mode == 'workflow':
    print('The configured source is GitHub Actions; the artifact deployment job will publish it.')
else:
    if source.get('branch') != 'gh-pages' or source.get('path') not in ['/', None]:
        raise SystemExit('Pages is not configured for gh-pages root. No settings were changed.')
    expected = api('/git/ref/heads/gh-pages')['object']['sha']
    api('/pages/builds', 'POST')
    for attempt in range(36):
        build = api('/pages/builds/latest')
        print(json.dumps({'attempt': attempt+1, 'status': build.get('status'), 'commit': build.get('commit')}, ensure_ascii=False))
        if build.get('commit') == expected:
            if build.get('status') == 'built':
                break
            if build.get('status') == 'errored':
                raise SystemExit('Pages build failed: ' + str(build.get('error')))
        time.sleep(5)
    else:
        raise SystemExit('Timed out awaiting the actual Pages build; publication is not verified.')
