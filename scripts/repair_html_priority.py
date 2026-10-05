#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil
from pathlib import Path
from archive_inbox import ROOT, entries, choose_entry, inventory, jwrite

RUN=ROOT/'.archive-run'
REPORT=RUN/'html-priority-repair.json'

def sha(data: bytes):
    return hashlib.sha256(data).hexdigest()

def copy_source_tree_to_root(source: Path, record: Path):
    """Preserve ZIP/folder paths at the record root so original HTML relative links keep working."""
    for p in entries(source):
        rel=p.relative_to(source)
        dst=record/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        if p.resolve()!=dst.resolve():
            shutil.copy2(p,dst)

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

        source=record/'source'
        meta_path=record/'archive.json'
        if source.is_dir():
            htmls=[p for p in entries(source) if p.suffix.lower() in {'.html','.htm'}]
            if not htmls:
                skipped.append({'slug':record.name,'reason':'no-html-source'}); continue
            meta=json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.is_file() else {}
            chosen=choose_entry(source,meta)
            copy_source_tree_to_root(source,record)
            root_chosen=record/chosen.relative_to(source)
            (record/'index.html').write_bytes(root_chosen.read_bytes())
            files=[x for x in inventory(record) if x['path']!='archive-manifest.json']
            manifest={**manifest,'files':files,'entryPolicy':'html-exact-v2','entrySource':chosen.relative_to(source).as_posix()}
            jwrite(manifest_path,manifest)
            after=(record/'index.html').read_bytes()
            repaired.append({'slug':record.name,'layout':'source-dir','entry':manifest['entrySource'],'indexSha256':sha(after),'url':'https://softm.github.io/hwagok-farm/records/'+record.name+'/'})
            continue

        candidates=[p for p in record.iterdir() if p.is_file() and p.suffix.lower() in {'.html','.htm'} and p.name.lower() not in {'index.html','summary.html','history.html'}]
        if not candidates:
            skipped.append({'slug':record.name,'reason':'no-root-source-html'}); continue
        chosen=max(candidates,key=lambda p:(0 if p.name.lower()=='record.html' else 1,p.stat().st_size))
        (record/'index.html').write_bytes(chosen.read_bytes())
        after=(record/'index.html').read_bytes()
        manifest={**manifest,'entryPolicy':'html-exact-v2','entrySource':chosen.name}
        jwrite(manifest_path,manifest)
        repaired.append({'slug':record.name,'layout':'legacy-root','entry':chosen.name,'indexSha256':sha(after),'url':'https://softm.github.io/hwagok-farm/records/'+record.name+'/'})

    RUN.mkdir(parents=True,exist_ok=True)
    jwrite(REPORT,{'schemaVersion':2,'policy':'html-exact-v2','repaired':repaired,'skipped':skipped})
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a') as out:
            out.write('count='+str(len(repaired))+'\n')
    print(json.dumps({'repaired':len(repaired),'skipped':len(skipped)},ensure_ascii=False))

if __name__=='__main__':
    main()
