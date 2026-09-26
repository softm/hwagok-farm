#!/usr/bin/env python3
"""Build the manual-start archive from checksum-verified web-image source data."""
from pathlib import Path
import base64, hashlib, html, json, math, shutil, struct, subprocess, tempfile, zipfile, zlib

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'cultivator-manual-start-20260922'
SOURCE = ROOT / 'archive/media-transfers' / SLUG
OUT = ROOT / 'public/archive' / SLUG
NAMES = ['01-main-clutch-off.png','02-rotary-clutch-off.png','03-gear-neutral.png','04-fuel-valve-on.png','05-throttle-middle.png','06-choke-closed.png','07-engine-switch-run.png','08-recoil-take-up.png','09-recoil-start.png','10-choke-open.png']
STEPS = [('주클러치 레버','끊김','주클러치 레버를 끊김으로 둡니다.'),('로터리 클러치 레버','끊김','주클러치와 별도로 로터리 클러치도 끊김인지 확인합니다.'),('변속레버','중립','실제 기체 안내판의 중립 위치를 확인합니다.'),('연료코크','열림(ON)','연료코크와 초크는 서로 다른 조작부입니다.'),('조속레버','중간','교육 화면에 표시된 중간 위치입니다. 변속 중립과 구분합니다.'),('기화기 초크레버','닫힘','첨부 교육자료의 시동 준비 단계입니다.'),('전환 스위치','운전','운전 위치로 조작합니다. 같은 스위치의 정지 표시도 확인합니다.'),('리코일 스타트 로프','가볍게 당김','압축 저항이 느껴질 때까지 가볍게 당깁니다.'),('리코일 스타트 로프','시동 당김','준비 당김에 이어 시동을 위한 당김으로 진행합니다. 반드시 두 번 시도하라는 뜻은 아닙니다.'),('시동 후 초크레버','열림으로 복귀','시동 후에는 안쪽으로 넣어 열림으로 되돌립니다. 레버를 넣는 것과 초크를 닫는 것을 혼동하지 않습니다.')]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def decode_sources():
    repairs_file = SOURCE / 'repairs.json'
    repairs = json.loads(repairs_file.read_text()) if repairs_file.exists() else {}
    chunks, errors = [], []
    for n in range(17):
        path = SOURCE / f'{n:02}.txt'
        lines = path.read_text().splitlines()
        _, number, length, digest = lines[0].split()
        length = int(length)
        blocks = {}
        for line in lines[1:]:
            parts = line.split()
            if len(parts) != 3:
                continue
            key, crc, encoded = parts
            replacement = repairs.get(f'{n:02}:{key}')
            if replacement:
                crc, encoded = replacement.split()
            try:
                data = base64.b64decode(encoded, validate=True)
                if f'{zlib.crc32(data):08x}' != crc:
                    raise ValueError('CRC mismatch')
                blocks[key] = data
            except Exception:
                print(f'Invalid source block: {n:02}:{key}', flush=True)
        count = math.ceil(length / 384)
        for start in range(0, count, 4):
            group = list(range(start, min(start + 4, count)))
            missing = [i for i in group if f'{i:02}' not in blocks]
            parity = blocks.get(f'P{start // 4:02}')
            if len(missing) == 1 and parity is not None and len(parity) == 384:
                recovered = bytearray(parity)
                for i in group:
                    if i != missing[0]:
                        for j, value in enumerate(blocks[f'{i:02}']):
                            recovered[j] ^= value
                i = missing[0]
                blocks[f'{i:02}'] = bytes(recovered[:min(384, length - i * 384)])
                print(f'Recovered and hash-checked block: {n:02}:{i:02}', flush=True)
            elif missing:
                errors.append(f'{n:02}: missing {missing}; valid parity={parity is not None}')
        if any(f'{i:02}' not in blocks for i in range(count)):
            continue
        data = b''.join(blocks[f'{i:02}'] for i in range(count))[:length]
        if sha(data) != digest:
            errors.append(f'{n:02}: chunk SHA256 mismatch')
        chunks.append(data)
    if errors:
        raise RuntimeError('IMAGE TRANSFER VALIDATION FAILED: ' + '; '.join(errors))
    packed = b''.join(chunks)
    assert len(packed) == 50031
    assert sha(packed) == 'e13e19ccc691d785b77f9b20b5e8ee45a275d0112cc8c3b74166bdf7816e6a92'
    data = zlib.decompress(packed)
    assert sha(data) == '021fe92b0987c7175011350d83efeda0969fc7820d27963b5798a33fedecc7df'
    return data

def main():
    data = decode_sources()
    if not shutil.which('ffmpeg'):
        subprocess.run(['sudo','apt-get','update','-qq'], check=True)
        subprocess.run(['sudo','apt-get','install','-y','ffmpeg'], check=True)
    images = OUT / 'images'
    images.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        (temporary / 'frames.mkv').write_bytes(data)
        subprocess.run(['ffmpeg','-v','error','-i',str(temporary/'frames.mkv'),'-vsync','0','-start_number','0',str(temporary/'%02d.png')], check=True)
        frames = sorted(temporary.glob('*.png'))
        assert len(frames) == 10, f'Expected 10 frames, got {len(frames)}'
        for frame, original in enumerate([0,6,1,4,2,3,5,9,7,8]):
            shutil.copyfile(frames[frame], images / NAMES[original])
    media = []
    for name in NAMES:
        contents = (images / name).read_bytes()
        assert contents.startswith(b'\x89PNG\r\n\x1a\n')
        width, height = struct.unpack('>II', contents[16:24])
        assert (width, height) == (959, 544)
        media.append({'file':'images/'+name,'sha256':sha(contents),'bytes':len(contents),'width':width,'height':height})
    manifest = {'slug':SLUG,'expectedImages':10,'publishedImages':10,'status':'web-images-complete','imageType':'web-optimized derivatives, not byte-identical original PNGs','sourceVideo':'https://www.youtube.com/watch?v=POKGZK2ds34','transportSHA256':sha(data),'media':media}
    (OUT / 'image_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    rows = ''.join(f'<tr><td>{i+1:02}</td><td>{html.escape(a)}</td><td><strong>{html.escape(b)}</strong></td></tr>' for i,(a,b,c) in enumerate(STEPS))
    figures = ''.join(f'<article id="step-{i+1}" class="step"><div class="stephead"><span class="number">{i+1:02}</span><div><h3>{html.escape(a)} · {html.escape(b)}</h3><p>{html.escape(c)}</p></div></div><button class="photo" aria-label="사진 {i+1} 확대"><img src="images/{NAMES[i]}" alt="{html.escape(a)} {html.escape(b)}" width="959" height="544" loading="lazy"></button><p class="caption">사진 {i+1:02} · 사용자 제공 교육영상 캡처의 웹 최적화본</p></article>' for i,(a,b,c) in enumerate(STEPS))
    page = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>아세아 관리기 수동 시동·정지 | 화곡농장</title><meta name="description" content="사진 10장으로 정리한 아세아 관리기 수동 시동 순서. 시동 후 초크는 열림, 사진 속 레버는 안쪽으로 넣습니다."><style>
:root{color-scheme:light;--ink:#19352c;--muted:#53665e;--line:#d9e0d9;--paper:#f5f4ed;--green:#24553e}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;line-height:1.75}a{color:inherit}nav{padding:16px max(20px,calc((100vw - 1080px)/2));background:#fff;display:flex;gap:22px;flex-wrap:wrap;font-size:14px}header{background:var(--ink);color:white;padding:62px 24px 54px}.inner,main{max-width:1080px;margin:auto}.eyebrow{font-size:12px;letter-spacing:.18em;font-weight:700}h1{font-size:clamp(30px,5vw,52px);line-height:1.3;letter-spacing:-.04em;margin:18px 0}header p{max-width:710px;color:#d4e1d7}.badges{display:flex;gap:8px;flex-wrap:wrap}.badges span{border:1px solid #6e8778;border-radius:30px;padding:5px 14px;font-size:13px}main{padding:32px 20px 60px}section{margin:0 0 40px}h2{font-size:25px;line-height:1.45}h3{font-size:20px;line-height:1.45;margin:0 0 6px}.callout{background:#e6efdf;border-left:5px solid #567443;padding:24px;border-radius:0 14px 14px 0}.callout h2{margin:0 0 10px}.callout strong{font-size:23px}.actions{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0}.actions a,.close{background:var(--green);color:white;border:0;border-radius:8px;padding:12px 18px;text-decoration:none;font:inherit;font-weight:650}.tablewrap{overflow:auto;background:#fff;border-radius:12px;border:1px solid var(--line)}table{width:100%;border-collapse:collapse;min-width:390px;text-align:left}th{background:#e8ece3}th,td{padding:12px 16px;border-bottom:1px solid var(--line)}.step{background:white;border:1px solid var(--line);border-radius:16px;margin:22px 0;overflow:hidden;scroll-margin-top:20px}.stephead{padding:24px;display:flex;gap:20px;align-items:flex-start}.stephead p{margin:0;color:var(--muted)}.number{font-size:31px;font-weight:750;color:#6a7e60;line-height:1.3}.photo{display:block;width:100%;padding:0;border:0;background:#e4e8df;cursor:zoom-in}.photo img{width:100%;height:auto;display:block}.caption{padding:0 24px;font-size:13px;color:var(--muted)}.notice{background:#fff4df;border:1px solid #ddc89a;padding:24px;border-radius:14px}footer{border-top:1px solid var(--line);padding-top:24px;font-size:14px;color:var(--muted)}dialog{border:0;padding:12px;background:#17271f;color:white;max-width:96vw;max-height:96vh;border-radius:10px}dialog::backdrop{background:#000d}dialog img{display:block;max-width:90vw;max-height:78vh;object-fit:contain}dialog .close{display:block;margin:10px 0 0 auto;cursor:pointer}:focus-visible{outline:3px solid #ba682c;outline-offset:4px}@media(max-width:600px){header{padding:35px 20px}.stephead{padding:18px;gap:12px}.callout{padding:20px}.callout strong{font-size:20px}h3{font-size:18px}th,td{padding:10px}.actions a{flex:1;text-align:center}.caption{padding:0 18px}}@media print{nav,.actions,dialog{display:none}header{background:white;color:#19352c;padding:0}header p{color:#19352c}body{background:white}.step{break-inside:avoid}.photo{cursor:default}main{padding:20px 0}}
</style></head><body><nav><a href="https://softm.github.io/hwagok-farm/">화곡농장 홈</a><a href="https://softm.github.io/projects/">전체 프로젝트</a><a href="#photos">사진별 순서</a></nav><header><div class="inner"><div class="eyebrow">HWAGOK FARM / MACHINE GUIDE</div><h1>아세아 관리기<br>수동 시동·정지</h1><p>사용자가 제공한 교육영상 캡처를 따라 조작 순서를 확인합니다. 시동 전의 설정과 시동 후 초크 복귀를 구분했습니다.</p><div class="badges"><span>2026.09.22 기록</span><span>사진 10장</span><span>수동 시동</span><span>GB290 표기 확인</span></div></div></header><main><section class="callout"><h2>시동 건 다음에 초크를 닫나요?</h2><strong>아니요. 시동 후에는 초크를 열림으로 되돌립니다.</strong><p>사진 속 조작부에서는 <b>레버를 안쪽으로 넣는 동작이 열림</b>입니다. 마지막 사진의 자막은 “시동후에 초크 밸브를 꼭 안쪽으로 넣어 주세요”입니다. 안쪽으로 넣는 것과 초크를 닫는 것을 혼동하지 않습니다.</p></section><div class="actions"><a href="https://www.youtube.com/watch?v=POKGZK2ds34" target="_blank" rel="noopener">원본 교육영상 ↗</a><a href="record.md" download>Markdown</a><a href="manual-start-20260922-web.zip" download>사진 포함 웹판 ZIP</a></div><section><h2>01. 시동 순서 한눈에 보기</h2><div class="tablewrap"><table><thead><tr><th>순서</th><th>조작부</th><th>설정·행동</th></tr></thead><tbody>__ROWS__</tbody></table></div><p>01~03은 모두 시동 전에 확인할 상태입니다. 조작 방향은 사진 속 기종 기준이며 실제 기체 표시를 우선합니다.</p></section><section id="photos"><h2>02. 사진으로 따라가기</h2><p>사진을 누르면 확대됩니다. 처음 첨부한 10장 전체를 순서대로 배치했습니다.</p>__FIGURES__</section><section><h2>03. 초크 설정 구분</h2><div class="tablewrap"><table><thead><tr><th>상황</th><th>초크</th><th>사진 속 레버</th></tr></thead><tbody><tr><td>교육자료의 시동 준비</td><td>닫힘</td><td>바깥으로 당긴 상태</td></tr><tr><td>시동 후</td><td><b>열림</b></td><td><b>안쪽으로 넣음</b></td></tr><tr><td>정상 운전</td><td>열림 유지</td><td>안쪽으로 넣어 둠</td></tr></tbody></table></div><p>마지막 캡처의 파일명과 자막에는 시동이 안 될 때 초크를 열림 쪽으로 두고 다시 당기는 안내도 포함되어 있습니다. 다른 엔진에 같은 레버 방향을 그대로 적용하지 않습니다.</p></section><section class="notice"><h2>04. 정지 — 기존 대화의 보충 설명</h2><p><b>첨부 10장은 수동 시동 장면이며, 정지 순서를 촬영한 자료는 아닙니다.</b> 아래는 기존 대화에서 별도로 설명했던 내용입니다. 실제 기체 표시와 전용 설명서를 우선합니다.</p><p><b>동력 끊기 → 기계가 멈춘 뒤 중립 → 조속 저속 → 전환 스위치 정지 → 엔진 정지 후 연료코크 닫힘.</b></p><p>사진 07은 운전 조작 장면입니다. 같은 스위치의 정지 위치를 찾는 데만 참고합니다. <a href="https://www.honda-engines-eu.com/files/files/owners-manual-gx120-160-200-ut1-english-32z4f605.pdf">일반 엔진 조작 보충 참고(Honda)</a>는 사진 속 GB290 전용 설명서가 아닙니다.</p></section><footer><h2>자료와 공개 범위</h2><p>기준 자료: 사용자 제공 아세아 교육영상 캡처 10장과 후속 초크 질문. 엔진 덮개의 GB290 표기만 확인되며 관리기 본체 모델명은 확정하지 않았습니다.</p><p><b>공개 사진과 웹판 ZIP은 웹 최적화본입니다.</b> 원본 PNG의 바이트와 동일하지 않습니다. 원본 PNG 10장과 기존 이미지 내장 HTML은 이 대화에서 제공한 원본 ZIP에 보존되어 있습니다. 원본 동영상 파일은 첨부되지 않아 YouTube 링크로 연결합니다.</p><p><a href="image_manifest.json">공개 사진 목록·파일 검증값</a> · <a href="https://softm.github.io/hwagok-farm/">화곡농장 홈</a> · <a href="https://softm.github.io/projects/">전체 프로젝트</a> · <a href="https://hwagok-farm-private.vercel.app/">비공개 사이트</a></p></footer></main><dialog id="zoom"><img alt="확대 사진"><button class="close">닫기</button></dialog><script>const d=document.querySelector('#zoom');let active;document.querySelectorAll('.photo').forEach(b=>b.addEventListener('click',()=>{active=b;const i=b.querySelector('img'),v=d.querySelector('img');v.src=i.src;v.alt=i.alt;d.showModal()}));d.querySelector('button').onclick=()=>d.close();d.addEventListener('close',()=>active?.focus());d.addEventListener('click',e=>{if(e.target===d)d.close()});</script></body></html>'''
    page = page.replace('__ROWS__', rows).replace('__FIGURES__', figures)
    (OUT / 'record.html').write_text(page, encoding='utf-8')
    assert (OUT / 'record.md').is_file(), 'Markdown source missing'
    zip_name = 'manual-start-20260922-web.zip'
    with zipfile.ZipFile(OUT / zip_name, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('index.html', page)
        for name in ['record.md','record.html','image_manifest.json']:
            archive.write(OUT/name, name)
        for name in NAMES:
            archive.write(images/name, 'images/'+name)
    record = {'slug':SLUG,'kind':'농기계·사용법','title':'2026-09-22 아세아 관리기 수동 시동·정지','description':'수동 시동 순서와 시동 후 초크 열림 복귀를 사진 10장으로 정리했습니다.','meta':['수동 시동·초크','웹 최적화 사진 10장','MD·HTML·사진 포함 ZIP'],'legacyPath':'/archive/'+SLUG+'/record.html','assets':{'md':'/archive/'+SLUG+'/record.md','html':'/archive/'+SLUG+'/record.html','zip':'/archive/'+SLUG+'/'+zip_name},'assetStatus':'사진 10장(웹 최적화본)·MD·HTML·ZIP 공개'}
    registry = ROOT / 'archive/records.ts'
    text = registry.read_text()
    marker = 'export const archiveRecords: ArchiveRecord[] = ['
    assert marker in text, 'Unexpected archive registry structure'
    if SLUG not in text:
        registry.write_text(text.replace(marker, marker+'\n'+json.dumps(record,ensure_ascii=False,indent=2)+',',1))
    print('MANUAL START ARCHIVE READY: 10 validated PNG images, HTML, MD, ZIP and project-home entry.', flush=True)

if __name__ == '__main__':
    main()
