#!/usr/bin/env python3
"""Import only the verified, self-contained Hwagok deodeok archive."""
from pathlib import Path, PurePosixPath
import hashlib, json, re, shutil, stat, sys, zipfile

SLUG = 'deodeok-harvest-20260923'
BUNDLE = Path('deodeok-20260923-complete.zip')
EXPECTED_SHA256 = '9b817586901d7a52222820158f16c79b234edfc3c522dbe1d53f1743914310d0'
TARGET = Path('public/archive') / SLUG

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    if not BUNDLE.is_file():
        print('No new deodeok bundle: keep existing archive unchanged.')
        return 0
    receipt_path = TARGET / 'import-receipt.json'
    if receipt_path.is_file() and json.loads(receipt_path.read_text()).get('sourceBundleSha256') == EXPECTED_SHA256:
        print('This verified bundle is already imported; later document edits are preserved.')
        return 0
    bundle_bytes = BUNDLE.read_bytes()
    if digest(bundle_bytes) != EXPECTED_SHA256:
        raise ValueError('Unexpected bundle SHA-256; no archive files were changed.')
    with zipfile.ZipFile(BUNDLE) as archive:
        items = [i for i in archive.infolist() if not i.is_dir()]
        if len(items) > 100 or sum(i.file_size for i in items) > 50_000_000:
            raise ValueError('Bundle exceeds the expected scope.')
        files = {}
        for item in items:
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or path.parts[0] != SLUG:
                raise ValueError(f'Unsafe archive path: {item.filename}')
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError('Symbolic links are not allowed.')
            rel = str(PurePosixPath(*path.parts[1:]))
            if rel in files or not rel or '\\' in rel:
                raise ValueError('Duplicate or invalid path.')
            files[rel] = archive.read(item)
    for required in ['record.html','record.md','record.json','index.html','checksums.sha256']:
        if required not in files:
            raise ValueError(f'Missing required document: {required}')
    for line in files['checksums.sha256'].decode('utf-8').splitlines():
        expected, rel = line.split('  ', 1)
        if rel not in files or digest(files[rel]) != expected:
            raise ValueError(f'Invalid checksum: {rel}')
    record = json.loads(files['record.json'])
    media = record['media']
    if record['slug'] != SLUG or record['visibility'] != 'public':
        raise ValueError('Wrong archive identity or visibility.')
    if sum(m['type']=='image' for m in media) != 7 or sum(m['type']=='video' for m in media) != 3:
        raise ValueError('Expected exactly 7 original images and 3 original videos.')
    for m in media:
        if m['file'] not in files or digest(files[m['file']]) != m['sha256']:
            raise ValueError(f"Original-media mismatch: {m['name']}")
        if m['type'] == 'video':
            for field in ['playback','poster']:
                if m[field] not in files:
                    raise ValueError(f'Missing video {field}.')
    manifest_path = Path('archive/records.ts')
    source = manifest_path.read_text(encoding='utf-8')
    match = re.search(r'export\s+const\s+archiveRecords\s*:\s*ArchiveRecord\[\]\s*=\s*', source)
    if not match:
        raise ValueError('Central manifest format changed; automatic overwrite refused.')
    records, consumed = json.JSONDecoder().raw_decode(source[match.end():])
    matches = [r for r in records if r['slug'] == SLUG]
    if len(matches) != 1:
        raise ValueError('Expected exactly one existing deodeok entry.')
    matches[0].update(
        description='채취한 삭과, 12시대 뿌리 굴취 현장, 13시대 수확물의 원본 사진 7장과 영상 3개를 함께 보존한 기록입니다.',
        meta=['사진 원본 7장','영상 원본 3개 · 재생용 3개','MD · HTML · ZIP · 체크섬'],
        assets={'md':f'/archive/{SLUG}/record.md','html':f'/archive/{SLUG}/record.html','zip':f'/archive/{SLUG}/bundle.zip'},
        assetStatus='complete',
    )
    updated = source[:match.end()] + json.dumps(records, ensure_ascii=False, indent=2) + source[match.end()+consumed:]
    TARGET.mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        destination = TARGET / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + '.tmp')
        temporary.write_bytes(data)
        temporary.replace(destination)
    shutil.copyfile(BUNDLE, TARGET / 'bundle.zip')
    manifest_path.write_text(updated, encoding='utf-8')
    receipt_path.write_text(json.dumps({'sourceBundleSha256': EXPECTED_SHA256, 'originalImages': 7, 'originalVideos': 3}, indent=2) + '\n')
    print(f'Imported {SLUG}: 7 original JPG, 3 original MP4, 3 playback MP4, MD, HTML, ZIP.')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'Archive import stopped: {exc}', file=sys.stderr)
        raise SystemExit(1)
