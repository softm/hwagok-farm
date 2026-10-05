#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from archive_inbox import ROOT, entries, choose_entry, render, inventory, jwrite

RUN=ROOT/'.archive-run'
REPORT=RUN/'html-priority-repair.json'

def digest_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()

def main():
    repaired=[]
    skipped=[]
    records=ROOT/'public/records'
    for record in sorted(records.iterdir()) if records.is_dir() else []:
        if not record.is_dir():
            continue
        source=record/'source'
        meta_path=record/'archive.json'
        manifest_path=record/'archive-manifest.json'
        if not source.is_dir() or not meta_path.is_file() or not manifest_path.is_file():
            skipped.append({'slug':record.name,'reason':'legacy-or-no-source'})
            continue
        htmls=[p for p in entries(source) if p.suffix.lower() in {'.html','.htm'}]
        if not htmls:
            skipped.append({'slug':record.name,'reason':'no-html-source'})
            continue
        meta=json.loads(meta_path.read_text(encoding='utf-8'))
        chosen=choose_entry(source,meta)
        if chosen.suffix.lower() not in {'.html','.htm'}:
            raise RuntimeError('HTML exists but choose_entry did not select HTML: '+record.name)
        before=(record/'index.html').read_bytes() if (record/'index.html').is_file() else b''
        metadata=render(source,record,meta,meta['date'],record.name)
        jwrite(meta_path,metadata)
        old=json.loads(manifest_path.read_text(encoding='utf-8'))
        files=[x for x in inventory(record) if x['path']!='archive-manifest.json']
        new={**old,'metadata':metadata,'files':files,'entryPolicy':'html-first-v1','entrySource':chosen.relative_to(source).as_posix()}
        jwrite(manifest_path,new)
        after=(record/'index.html').read_bytes()
        if before!=after or old.get('entryPolicy')!='html-first-v1' or old.get('entrySource')!=new['entrySource']:
            repaired.append({'slug':record.name,'entry':new['entrySource'],'indexSha256':digest_bytes(after),'url':metadata['url']})
    RUN.mkdir(parents=True,exist_ok=True)
    jwrite(REPORT,{'schemaVersion':1,'policy':'html-first-v1','repaired':repaired,'skipped':skipped})
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a') as out:
            out.write('count='+str(len(repaired))+'\n')
    print(json.dumps({'repaired':len(repaired),'skipped':len(skipped)},ensure_ascii=False))

if __name__=='__main__':
    main()
