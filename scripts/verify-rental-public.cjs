/* Independent production verification: actual bytes, image decoding, video playback. */
const fs = require('node:fs');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const manifest = require('../archive/farm-machine-rental-20260924.manifest.json');
const base = 'https://softm.github.io/hwagok-farm';
const record = `${base}/archive/${manifest.record}`;
const pageUrl = `${base}/${manifest.record}/`;
const report = { pageUrl, checkedAt: new Date().toISOString(), assets: [], images: [], videos: [] };
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
async function get(url, options = {}) {
  return fetch(url, { ...options, signal: AbortSignal.timeout(30000) });
}
async function main() {
  const expectedManifest = sha(fs.readFileSync('archive/farm-machine-rental-20260924.manifest.json'));
  let published = false;
  for (let attempt = 0; attempt < 30; attempt++) {
    try {
      const r = await get(`${record}/import-receipt.json?verify=${Date.now()}`);
      if (r.ok && (await r.json()).manifestSha256 === expectedManifest) { published = true; break; }
    } catch (_) { /* Allow publication and CDN propagation time. */ }
    await pause(10000);
  }
  if (!published) throw new Error('The verified bundle has not appeared on the production site.');
  for (const item of manifest.files) {
    const r = await get(`${record}/${item.path}?verify=${expectedManifest.slice(0, 12)}`);
    if (r.status !== 200) throw new Error(`${item.path}: HTTP ${r.status}`);
    const bytes = Buffer.from(await r.arrayBuffer());
    if (bytes.length !== item.bytes || sha(bytes) !== item.sha256) throw new Error(`${item.path}: byte verification failed`);
    const type = r.headers.get('content-type') || '';
    if (item.path.endsWith('.jpg') && !type.startsWith('image/jpeg')) throw new Error(`${item.path}: wrong MIME ${type}`);
    if (item.path.endsWith('.mp4') && !type.startsWith('video/mp4')) throw new Error(`${item.path}: wrong MIME ${type}`);
    report.assets.push({ path: item.path, status: r.status, bytes: bytes.length, contentType: type, sha256: item.sha256 });
  }
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const response = await page.goto(pageUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    if (!response || response.status() !== 200) throw new Error('The record page did not return HTTP 200.');
    const images = page.locator(`img[src*="/archive/${manifest.record}/assets/"]`);
    if (await images.count() !== manifest.expectedPhotos) throw new Error('Incorrect rendered photograph count.');
    for (let i = 0; i < await images.count(); i++) {
      const image = images.nth(i);
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(img => img.decode());
      const info = await image.evaluate(img => ({ src: img.currentSrc, width: img.naturalWidth, height: img.naturalHeight, complete: img.complete }));
      if (!info.complete || !info.width || !info.height) throw new Error(`Image ${i + 1} failed to decode.`);
      report.images.push(info);
    }
    const videos = page.locator('video');
    if (await videos.count() !== manifest.expectedVideos) throw new Error('Incorrect rendered video count.');
    for (let i = 0; i < await videos.count(); i++) {
      const video = videos.nth(i);
      await video.scrollIntoViewIfNeeded();
      await video.evaluate(async el => {
        el.muted = true;
        await Promise.race([el.play(), new Promise((_, reject) => setTimeout(() => reject(new Error('Video play timeout')), 15000))]);
      });
      await page.waitForTimeout(500);
      const info = await video.evaluate(el => ({ src: el.currentSrc, width: el.videoWidth, height: el.videoHeight, duration: el.duration, currentTime: el.currentTime, error: el.error?.message || null }));
      await video.evaluate(el => el.pause());
      if (info.error || !info.width || info.currentTime <= 0) throw new Error(`Video ${i + 1} did not actually play.`);
      report.videos.push(info);
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(200);
    report.mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    if (report.mobileOverflow) throw new Error('Mobile page has horizontal overflow.');
    await page.screenshot({ path: 'rental-media-mobile.png', fullPage: true });
    report.success = true;
  } finally { await browser.close(); }
}
main().catch(error => { report.success = false; report.error = String(error); process.exitCode = 1; }).finally(() => {
  fs.writeFileSync('rental-media-verification.json', JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
});
