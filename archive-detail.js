/* Progressive enhancement only: records and media remain readable without JavaScript. */
(() => {
  'use strict';
  if (window.__recordDetailInstalled) return;
  window.__recordDetailInstalled = true;
  let dialog, index = 0, images = [], opener;
  const allowedImage = img => { try { return ['https:', 'http:'].includes(new URL(img.currentSrc || img.src, location.href).protocol); } catch { return false; } };
  function viewer() {
    if (dialog) return dialog;
    dialog = document.createElement('dialog');
    dialog.className = 'record-viewer';
    dialog.setAttribute('aria-label', '기록 사진 확대 보기');
    dialog.innerHTML = '<div class="record-viewer-bar"><span data-counter aria-live="polite"></span><button type="button" data-close autofocus>닫기 ×</button></div><img alt=""><div class="record-viewer-bar"><button type="button" data-prev>← 이전</button><a target="_blank" rel="noopener noreferrer">원본 보기</a><button type="button" data-next>다음 →</button></div><p data-caption></p>';
    document.body.append(dialog);
    dialog.querySelector('[data-close]').onclick = () => dialog.close();
    dialog.querySelector('[data-prev]').onclick = () => show(index - 1);
    dialog.querySelector('[data-next]').onclick = () => show(index + 1);
    dialog.addEventListener('keydown', e => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); show(index + (e.key === 'ArrowRight' ? 1 : -1)); } });
    dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { opener?.focus({preventScroll:true}); });
    return dialog;
  }
  function show(next) {
    if (!images.length) return;
    index = (next + images.length) % images.length;
    const image = images[index], box = viewer();
    box.querySelector('img').src = image.currentSrc || image.src;
    box.querySelector('img').alt = image.alt || '기록 사진';
    box.querySelector('a').href = image.currentSrc || image.src;
    box.querySelector('[data-counter]').textContent = `${index + 1} / ${images.length}`;
    box.querySelector('[data-caption]').textContent = image.closest('figure')?.querySelector('figcaption')?.textContent || image.alt || '';
    box.querySelectorAll('[data-prev],[data-next]').forEach(b => b.disabled = images.length < 2);
    if (!box.open) box.showModal();
  }
  function enhance() {
    const root = document.querySelector('[data-record-page],.detail-page,.record-page');
    if (!root || !document.documentElement.hasAttribute('data-record-detail')) return;
    if (root.dataset.detailEnhanced) return;
    root.dataset.detailEnhanced = 'compact-v1';
    if (dialog?.open) dialog.close();
    const title = root.querySelector('h1');
    if (title) document.title = `${title.textContent.replace(/\s+/g, ' ').trim()} · 화곡농장`;
    const sections = [...root.querySelectorAll('.content-section,.record-section')].filter(s => s.querySelector('h2'));
    if (sections.length >= 4 && !root.querySelector('.record-toc')) {
      const nav = document.createElement('nav'); nav.className = 'record-toc'; nav.setAttribute('aria-label','상세 기록 목차');
      const label = document.createElement('b'); label.textContent = '바로가기'; nav.append(label);
      sections.forEach((s,i) => { if (!s.id) s.id = `record-section-${i+1}`; const a = document.createElement('a'); a.href = `#${s.id}`; a.textContent = s.querySelector('h2').textContent.trim(); nav.append(a); });
      const header = root.querySelector('.detail-hero,.record-header');
      if (header) header.after(nav);
    }
    for (const img of root.querySelectorAll('.archive-media-grid img,.record-gallery img,.photo-grid img,.gallery-grid img,.media-grid img')) {
      img.loading = 'lazy'; img.decoding = 'async';
      if (img.closest('button,a,[role="button"]') || !allowedImage(img)) continue;
      img.dataset.recordZoom = 'true'; img.tabIndex = 0; img.setAttribute('role','button'); img.setAttribute('aria-haspopup','dialog');
      img.setAttribute('aria-label', `사진 크게 보기: ${img.alt || '기록 사진'}`);
    }
  }
  function activate(image) { images = [...document.querySelectorAll('img[data-record-zoom]')].filter(allowedImage); opener = image; show(images.indexOf(image)); }
  document.addEventListener('click', e => { if (e.target instanceof HTMLImageElement && e.target.matches('img[data-record-zoom]')) activate(e.target); });
  document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target instanceof HTMLImageElement && e.target.matches('img[data-record-zoom]')) { e.preventDefault(); activate(e.target); } });
  document.addEventListener('DOMContentLoaded', enhance);
  window.addEventListener('archive:detail-ready', enhance);
  window.addEventListener('pageshow', enhance);
  enhance();
})();
