#!/usr/bin/env python3
import hashlib, html, json, os, re, shutil, sys, tempfile, unicodedata, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INBOX=ROOT/'zip'
RECORDS=ROOT/'public'/'records'
INDEX=ROOT/'index.html'
IMAGE={'.jpg','.jpeg','.png','.webp','.gif','.avif','.heic'}
VIDEO={'.mp4','.webm','.mov','.m4v'}
AUDIO={'.mp3','.m4a','.wav','.ogg','.flac','.aac'}
DOC={'.pdf','.txt','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.hwp','.hwpx'}
SKIP={'.DS_Store','Thumbs.db'}

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def safe_extract(z, dst):
    with zipfile.ZipFile(z) as f:
        for i in f.infolist():
            n=Path(i.filename)
            if n.is_absolute() or '..' in n.parts: raise RuntimeError(f'unsafe zip path: {i.filename}')
        f.extractall(dst)

def clean_title(name):
    s=re.sub(r'\.zip$','',name,flags=re.I)
    s=re.sub(r'^(\d{8}(?:-\d{4})?)[ _-]*','',s)
    s=re.sub(r'[_]+',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

def date_from(name):
    m=re.search(r'(20\d{2})(\d{2})(\d{2})',name)
    return f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else ''

def slugify(name):
    base=re.sub(r'\.zip$','',name,flags=re.I)
    date=re.search(r'(20\d{6})',base)
    d=date.group(1) if date else 'undated'
    rest=base[date.end():] if date else base
    rest=unicodedata.normalize('NFKC',rest).lower()
    tokens=re.findall(r'[a-z0-9]+',rest)
    if tokens:
        tail='-'.join(tokens)[:70]
    else:
        tail=hashlib.sha1(base.encode()).hexdigest()[:10]
    return f'{d}-{tail}'.strip('-')

def flatten_root(work):
    items=[p for p in work.iterdir() if p.name not in SKIP]
    while len(items)==1 and items[0].is_dir():
        work=items[0]; items=[p for p in work.iterdir() if p.name not in SKIP]
    return work

def manifest(src):
    out=[]
    for p in sorted(src.rglob('*')):
        if p.is_file() and p.name not in SKIP:
            out.append({'path':p.relative_to(src).as_posix(),'size':p.stat().st_size,'sha256':sha256(p)})
    return out

def pick_existing(src, suffix):
    candidates=[p for p in src.rglob('*') if p.is_file() and p.suffix.lower() in suffix]
    candidates.sort(key=lambda p:(0 if p.name.lower()=='index.html' else 1,len(p.parts),p.name))
    return candidates[0] if candidates else None

def generated_html(title,date,files):
    media=[]
    for x in files:
        p=x['path']; ext=Path(p).suffix.lower(); q=html.escape(p,quote=True); label=html.escape(Path(p).name)
        if ext in IMAGE: media.append(f'<figure><a href="{q}"><img src="{q}" loading="lazy" alt="{label}"></a><figcaption>{label}</figcaption></figure>')
        elif ext in VIDEO: media.append(f'<figure><video controls preload="metadata" src="{q}"></video><figcaption><a href="{q}">{label}</a></figcaption></figure>')
        elif ext in AUDIO: media.append(f'<p><audio controls preload="metadata" src="{q}"></audio> <a href="{q}">{label}</a></p>')
    docs=''.join(f'<li><a href="{html.escape(x["path"],quote=True)}">{html.escape(x["path"])}</a></li>' for x in files if Path(x['path']).suffix.lower() in DOC or Path(x['path']).suffix.lower() in {'.md','.html'})
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:auto;padding:24px;line-height:1.65}}img,video{{max-width:100%;height:auto}}.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}figure{{margin:0}}code{{word-break:break-all}}</style></head><body><p><a href="../../../">← 화곡농장 공개 아카이브</a></p><h1>{html.escape(title)}</h1><p>{html.escape(date)}</p><div class="gallery">{''.join(media)}</div><h2>문서·원본</h2><ul>{docs}</ul></body></html>'''

def generated_md(title,date,files):
    return '# '+title+'\n\n- 날짜: '+date+'\n- 원본 파일: '+str(len(files))+'개\n\n## 원본 파일\n\n'+''.join(f'- [{x["path"]}]({x["path"]}) — {x["size"]} bytes — SHA-256 `{x["sha256"]}`\n' for x in files)

def process(item):
    name=item.name; slug=slugify(name); date=date_from(name); title=clean_title(name)
    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/'src'; work.mkdir()
        if item.is_file():
            if item.suffix.lower()!='.zip': return None
            safe_extract(item,work)
        else:
            shutil.copytree(item,work,dirs_exist_ok=True)
        src=flatten_root(work)
        files=manifest(src)
        if not files: raise RuntimeError(f'empty input: {name}')
        target=RECORDS/slug
        if target.exists():
            old=target/'archive-manifest.json'
            if old.exists():
                try:
                    oldj=json.loads(old.read_text())
                    if oldj.get('inputSha256')==(sha256(item) if item.is_file() else None):
                        return {'skip':True,'item':item,'slug':slug}
                except Exception: pass
            # Never destroy an existing canonical record automatically.
            raise RuntimeError(f'target exists and differs: {slug}')
        shutil.copytree(src,target)
        mf={'schemaVersion':1,'source':name,'inputSha256':sha256(item) if item.is_file() else None,'date':date,'title':title,'slug':slug,'files':files}
        (target/'archive-manifest.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2))
        if not (target/'index.html').exists():
            (target/'index.html').write_text(generated_html(title,date,files))
        if not any(p.suffix.lower()=='.md' for p in target.iterdir() if p.is_file()):
            (target/'summary.md').write_text(generated_md(title,date,files))
        return {'skip':False,'item':item,'slug':slug,'date':date,'title':title,'files':len(files)}

def update_index(results):
    text=INDEX.read_text()
    m=re.search(r'(<script id="archive-data" type="application/json">)(.*?)(</script>)',text,re.S)
    if not m: raise RuntimeError('archive-data not found')
    data=json.loads(m.group(2)); by={x.get('dir'):x for x in data}
    for r in results:
        if r.get('skip'): continue
        by[r['slug']]={'date':r['date'],'kind':'아카이브','title':r['title'],'dir':r['slug'],'desc':f'수집함 원본 {r["files"]}개 파일을 보존한 공개 아카이브 기록.','url':f'https://softm.github.io/hwagok-farm/records/{r["slug"]}/','repoUrl':f'https://github.com/softm/hwagok-farm/tree/main/public/records/{r["slug"]}'}
    rows=sorted(by.values(),key=lambda x:(x.get('date',''),x.get('title','')),reverse=True)
    INDEX.write_text(text[:m.start(2)]+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+text[m.end(2):])

def main():
    RECORDS.mkdir(parents=True,exist_ok=True)
    if not INBOX.exists(): return
    items=sorted([p for p in INBOX.iterdir() if p.name not in SKIP])
    results=[]; errors=[]
    for item in items:
        try:
            r=process(item)
            if r: results.append(r)
        except Exception as e:
            errors.append(f'{item.name}: {e}')
    if results: update_index(results)
    # Delete only successfully processed inputs. Existing identical records may also clear their inbox copies.
    for r in results:
        item=r['item']
        if item.is_dir(): shutil.rmtree(item)
        elif item.exists(): item.unlink()
    if errors:
        print('\n'.join(errors),file=sys.stderr)
        # Keep failed inputs, but successful results remain staged for commit.
    print(json.dumps([{k:v for k,v in r.items() if k!='item'} for r in results],ensure_ascii=False,indent=2))
    if errors: sys.exit(2)

if __name__=='__main__': main()
