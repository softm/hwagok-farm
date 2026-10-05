#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from archive_inbox import ROOT, entries, choose_entry, render, inventory, jwrite

RUN=ROOT/'.archive-run'
REPORT=RUN/'html-priority-repair.json'

def sha(data: bytes):
    return hashlib.sha256(data).hexdigest()

def main():
    repaired=[]; skipped=[]
    records=ROOT/'public/records'
    for record in sorted(records.iterdir()) if records.is_dir() else []:
        if not record.is_dir():
            continue
        manifest_path=record/'archive-manifest.json'
        if not manifest_path.is_file():
            skipped.append({'slug':record.name,'reason':'no-manifest'}); continue
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        before=(record/'index.html').read_bytes() if (record/'index.html').is_file() else b''

        # New workflow layout: preserve source/ and render from HTML first.
        source=record/'source'
        meta_path=record/'archive.json'
        if source.is_dir() and meta_path.is_file():
            htmls=[p for p in entries(source) if p.suffix.lower() in {'.html','.htm'}]
            if not htmls:
                skipped.append({'slug':record.name,'reason':'no-html-source'}); continue
            meta=json.loads(meta_path.read_text(encoding='utf-8'))
            chosen=choose_entry(source,meta)
            metadata=render(source,record,meta,meta['date'],record.name)
            jwrite(meta_path,metadata)
            files=[x for x in inventory(record) if x['path']!='archive-manifest.json']
            manifest={**manifest,'metadata':metadata,'files':files,'entryPolicy':'html-first-v1','entrySource':chosen.relative_to(source).as_posix()}
            jwrite(manifest_path,manifest)
            after=(record/'index.html').read_bytes()
            repaired.append({'slug':record.name,'layout':'source-dir','entry':manifest['entrySource'],'indexSha256':sha(after),'url':metadata['url']})
            continue

        # Legacy ZIP layout: original HTML/MD live directly in the record folder.
        # index.html/summary.html/history.html are generated/derived pages and are never
        # selected as the source. record.html is acceptable when it is the only source HTML.
        candidates=[p for p in record.iterdir() if p.is_file() and p.suffix.lower() in {'.html','.htm'} and p.name.lower() not in {'index.html','summary.html','history.html'}]
        if not candidates:
            skipped.append({'slug':record.name,'reason':'no-root-source-html'}); continue
        chosen=max(candidates,key=lambda p:(0 if p.name.lower()=='record.html' else 1,p.stat().st_size))
        (record/'index.html').write_bytes(chosen.read_bytes())
        after=(record/'index.html').read_bytes()
        manifest={**manifest,'entryPolicy':'html-first-v1','entrySource':chosen.name}
        jwrite(manifest_path,manifest)
        repaired.append({'slug':record.name,'layout':'legacy-root','entry':chosen.name,'indexSha256':sha(after),'url':'https://softm.github.io/hwagok-farm/records/'+record.name+'/'})

    RUN.mkdir(parents=True,exist_ok=True)
    jwrite(REPORT,{'schemaVersion':2,'policy':'html-first-v1','repaired':repaired,'skipped':skipped})
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a') as out:
            out.write('count='+str(len(repaired))+'\n')
    print(json.dumps({'repaired':len(repaired),'skipped':len(skipped)},ensure_ascii=False))

if __name__=='__main__':
    main()
