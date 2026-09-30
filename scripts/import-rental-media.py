#!/usr/bin/env python3
"""Restore only this record's byte-verified original media and browser copies."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone

SLUG = 'farm-machine-rental-20260924'
ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / f'{SLUG}-complete.zip'
MANIFEST = ROOT / 'archive' / f'{SLUG}.manifest.json'
DEST = ROOT / 'public' / 'archive' / SLUG

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    if not BUNDLE.is_file():
        raise SystemExit(f'Required upload is missing: {BUNDLE.name}. No files were changed.')
    raw_manifest = MANIFEST.read_bytes()
    manifest = json.loads(raw_manifest)
    if manifest.get('record') != SLUG or manifest.get('version') != 1:
        raise SystemExit('Unexpected trusted manifest.')
    expected = manifest['files']
    allowed = {item['path'] for item in expected} | {'manifest.json'}
    verified: dict[str, bytes] = {}
    with zipfile.ZipFile(BUNDLE) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != allowed:
            raise SystemExit('Unexpected, missing or duplicate ZIP entries. Nothing was imported.')
        if archive.read('manifest.json') != raw_manifest:
            raise SystemExit('The bundle manifest differs from the trusted repository manifest.')
        for item in expected:
            name = item['path']
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                raise SystemExit(f'Unsafe archive path: {name}')
            info = archive.getinfo(name)
            if info.file_size != item['bytes']:
                raise SystemExit(f'Incorrect file size: {name}')
            data = archive.read(name)
            if len(data) != item['bytes'] or digest(data) != item['sha256']:
                raise SystemExit(f'Integrity verification failed: {name}')
            verified[name] = data
    DEST.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.rental-import-', dir=DEST.parent) as tmp:
        stage = Path(tmp)
        for name, data in verified.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        for name in verified:
            target = DEST / name
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage / name, target)
    (DEST / 'manifest.json').write_bytes(raw_manifest)
    receipt = {
        'record': SLUG, 'importedAt': datetime.now(timezone.utc).isoformat(),
        'originalPhotos': manifest['expectedPhotos'], 'originalVideos': manifest['expectedVideos'],
        'verifiedFileCount': len(verified), 'manifestSha256': digest(raw_manifest),
        'bundleSha256': digest(BUNDLE.read_bytes()),
    }
    shutil.copyfile(BUNDLE, DEST / 'bundle.zip')
    (DEST / 'import-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for item in expected:
        data = (DEST / item['path']).read_bytes()
        if digest(data) != item['sha256']:
            raise SystemExit(f'Post-import verification failed: {item["path"]}')
    BUNDLE.unlink()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
