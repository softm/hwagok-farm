// Preserve the supplied archive byte-for-byte. No new repository or branch is used.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { inflateRawSync } from 'node:zlib';

const slug = 'asea-engine-stop-20260922';
const base = `/archive/${slug}`;
const directory = path.join(process.cwd(), 'public', base);
const zipPath = path.join(directory, 'source.zip');
const expectedZipHash = '54b16715901581fd10e04b77e184fa05c53faa0041ebd29ddd8d25ea3261c84f';
const imageNames = ['01-main-clutch-off.png','02-rotary-clutch-off.png','03-throttle-low.png','04-travel-gear-neutral.png','05-tilling-gear-neutral.png','06-manual-stop-switch.png','07-electric-key-off.png'];
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const inline = value => escape(value).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/`([^`]+)`/g, '<code>$1</code>');
fs.mkdirSync(directory, {recursive:true});

function readVerifiedZip(bytes) {
  if (bytes.length !== 4547477 || hash(bytes) !== expectedZipHash) throw new Error('Engine-stop source.zip does not match the supplied original archive. Publication stopped.');
  let end = bytes.length - 22;
  const minimum = Math.max(0, bytes.length - 65557);
  for (; end >= minimum && bytes.readUInt32LE(end) !== 0x06054b50; end--) {}
  if (end < minimum) throw new Error('ZIP directory not found.');
  const count = bytes.readUInt16LE(end + 10);
  if (count !== 11) throw new Error(`Unexpected ZIP entry count: ${count}`);
  let offset = bytes.readUInt32LE(end + 16);
  const entries = new Map();
  for (let i = 0; i < count; i++) {
    if (bytes.readUInt32LE(offset) !== 0x02014b50) throw new Error('Invalid ZIP central directory.');
    const flags = bytes.readUInt16LE(offset + 8);
    const method = bytes.readUInt16LE(offset + 10);
    const compressedSize = bytes.readUInt32LE(offset + 20);
    const expandedSize = bytes.readUInt32LE(offset + 24);
    const nameSize = bytes.readUInt16LE(offset + 28);
    const extraSize = bytes.readUInt16LE(offset + 30);
    const commentSize = bytes.readUInt16LE(offset + 32);
    const localOffset = bytes.readUInt32LE(offset + 42);
    const name = bytes.subarray(offset + 46, offset + 46 + nameSize).toString('utf8');
    if ((flags & 1) || expandedSize > 2000000 || !name.startsWith('아세아_관리기_엔진정지/') || name.includes('..') || name.includes('\\')) throw new Error('Unsupported archive entry.');
    if (bytes.readUInt32LE(localOffset) !== 0x04034b50) throw new Error('Invalid ZIP local header.');
    const start = localOffset + 30 + bytes.readUInt16LE(localOffset + 26) + bytes.readUInt16LE(localOffset + 28);
    const compressed = bytes.subarray(start, start + compressedSize);
    const data = method === 0 ? compressed : method === 8 ? inflateRawSync(compressed, {maxOutputLength:2000000}) : null;
    if (!data || data.length !== expandedSize) throw new Error('ZIP entry size or compression mismatch.');
    entries.set(name.slice('아세아_관리기_엔진정지/'.length), data);
    offset += 46 + nameSize + extraSize + commentSize;
  }
  for (const name of ['index.html','엔진정지.md','README.txt','이미지목록.json', ...imageNames.map(n=>'images/'+n)]) {
    if (!entries.has(name)) throw new Error(`Missing original: ${name}`);
  }
  return entries;
}

const navigation = '<nav style="padding:14px 20px;background:#fff;border-bottom:1px solid #dce5df;display:flex;gap:18px;flex-wrap:wrap;font:14px/1.5 system-ui"><a href="../../">화곡농장 홈</a><a href="https://softm.github.io/projects/">전체 프로젝트</a><a href="./record.md">Markdown</a>';
let ready = false;
if (fs.existsSync(zipPath)) {
  const entries = readVerifiedZip(fs.readFileSync(zipPath));
  fs.mkdirSync(path.join(directory, 'images'), {recursive:true});
  for (const name of imageNames) {
    const data = entries.get('images/'+name);
    if (data.subarray(0,8).toString('hex') !== '89504e470d0a1a0a') throw new Error(`Invalid PNG: ${name}`);
    fs.writeFileSync(path.join(directory, 'images', name), data);
  }
  fs.writeFileSync(path.join(directory,'record.md'), entries.get('엔진정지.md'));
  fs.writeFileSync(path.join(directory,'README-original.txt'), entries.get('README.txt'));
  fs.writeFileSync(path.join(directory,'image-manifest.json'), entries.get('이미지목록.json'));
  const original = entries.get('index.html').toString('utf8');
  fs.writeFileSync(path.join(directory,'record.html'), original.replace(/<body([^>]*)>/i, match => match + navigation + '<a href="./source.zip" download>원본 ZIP · 사진 7장</a></nav>'));
  ready = true;
} else {
  const markdown = fs.readFileSync(path.join(directory,'record.md'),'utf8');
  let table = false;
  const body = markdown.split('\n').map(line => {
    if (line.startsWith('|')) {
      if (/^\|[\s:|-]+\|\s*$/.test(line)) return '';
      const cells = line.split('|').slice(1,-1).map(x=>`<td>${inline(x.trim())}</td>`).join('');
      const start = table ? '' : '<div class="table"><table>';
      table = true;
      return start + '<tr>'+cells+'</tr>';
    }
    const close = table ? '</table></div>' : ''; table = false;
    const image = line.match(/^!\[([^\]]*)\]\(([^)]*)\)$/);
    if (image) return close + `<figure class="pending"><b>원본 사진 전송 대기</b><figcaption>${escape(image[1])}</figcaption></figure>`;
    const heading = line.match(/^(#{1,6}) (.*)$/);
    if (heading) return close + `<h${heading[1].length}>${inline(heading[2])}</h${heading[1].length}>`;
    if (line.startsWith('> ')) return close + `<blockquote>${inline(line.slice(2))}</blockquote>`;
    if (line.startsWith('- ')) return close + `<p class="list">• ${inline(line.slice(2))}</p>`;
    return close + (line.trim() ? `<p>${inline(line)}</p>` : '');
  }).join('\n') + (table ? '</table></div>' : '');
  fs.writeFileSync(path.join(directory,'record.html'), `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>아세아 관리기 엔진 정지 · 원본 사진 전송 대기</title><style>*{box-sizing:border-box}body{margin:0;background:#f4f6f2;color:#18362d;font:16px/1.8 system-ui,-apple-system,sans-serif}main{max-width:960px;margin:24px auto 70px;padding:0 20px}a{color:#236b4e}h1{font-size:clamp(28px,5vw,44px);line-height:1.3}h2{margin-top:42px}h3{margin-top:32px}.notice,.pending,blockquote{border:1px solid #e3d4ab;background:#fff8e7;border-radius:12px;padding:16px 20px;margin:22px 0}.pending{background:white;color:#665b43}figcaption{margin-top:8px}.table{overflow-x:auto}table{width:100%;border-collapse:collapse;background:white}td{padding:10px;border:1px solid #d5dfd6;white-space:nowrap}tr:first-child{font-weight:700;background:#e6eee5}.list{margin:5px 0}code{overflow-wrap:anywhere}</style></head><body>${navigation}</nav><main><aside class="notice"><strong>사진 7장과 원본 ZIP은 아직 서버에 올라오지 않았습니다.</strong><br>아래는 본문 정리입니다. 원본 사진 대신 전송 대기 상태를 표시하며, 사진 포함 배포 완료로 처리하지 않았습니다.</aside>${body}</main></body></html>`);
}

const record = {
  slug,
  kind:'농기계·학습',
  title:'아세아 관리기 엔진 정지',
  description:'주 클러치·로타리 클러치 끊김, 조속 저속, 주행·갈이 중립 후 수동·전기시동형별 정지 조작을 정리했습니다.',
  meta:['2026-09-22 학습 정리','공통 5단계 · 형식별 정지', ready ? '원본 사진 7장 · MD · HTML · ZIP' : '사진 7장·원본 ZIP 서버 전송 대기'],
  legacyPath:base+'/record.html',
  assets:{md:base+'/record.md',html:base+'/record.html',...(ready?{zip:base+'/source.zip'}:{})},
  assetStatus: ready ? 'original-media-complete' : 'media-upload-pending'
};
const recordsPath = path.join(process.cwd(),'archive','records.ts');
const current = fs.readFileSync(recordsPath,'utf8');
const match = current.match(/export const archiveRecords: ArchiveRecord\[\] = ([\s\S]*);\s*$/);
if (!match) throw new Error('Archive registry format changed; refusing to overwrite it.');
const records = JSON.parse(match[1]).filter(r=>r.slug!==slug);
records.splice(Math.min(2,records.length),0,record);
fs.writeFileSync(recordsPath,current.slice(0,match.index)+'export const archiveRecords: ArchiveRecord[] = '+JSON.stringify(records,null,2)+';\n');
fs.writeFileSync(path.join(directory,'status.json'),JSON.stringify({slug,status:record.assetStatus,expectedImages:7,publishedImages:ready?7:0,sourceZip:ready?'source.zip':null,sourceZipSha256:ready?expectedZipHash:null},null,2)+'\n');
console.log(`Engine-stop archive: ${ready?'7 original PNG images and ZIP verified':'text only; 7 original images and ZIP still pending'}. Registry: ${records.length} records.`);
