(() => {
'use strict';
const links = [...document.querySelectorAll('[data-photo]')];
const modal = document.getElementById('photo-modal');
if (!modal || typeof modal.showModal !== 'function') return;
const image = document.getElementById('modal-image');
const title = document.getElementById('modal-title');
const caption = document.getElementById('modal-caption');
const count = document.getElementById('modal-count');
let current = 0, opener = null;
function show(index) {
 current = (index + links.length) % links.length;
 const link = links[current];
 image.src = link.href;
 image.alt = link.dataset.title;
 title.textContent = link.dataset.title;
 caption.textContent = link.dataset.caption;
 count.textContent = `${current + 1} / ${links.length}`;
}
links.forEach((link, index) => link.addEventListener('click', event => {
 event.preventDefault(); opener = link; show(index); modal.showModal();
 document.body.style.overflow = 'hidden';
}));
document.getElementById('modal-close').addEventListener('click', () => modal.close());
document.getElementById('modal-prev').addEventListener('click', () => show(current - 1));
document.getElementById('modal-next').addEventListener('click', () => show(current + 1));
modal.addEventListener('keydown', event => {
 if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
 if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
});
modal.addEventListener('click', event => {
 if (event.target === modal) {
  const r = modal.getBoundingClientRect();
  if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) modal.close();
 }
});
modal.addEventListener('close', () => {
 document.body.style.overflow = ''; if (opener) opener.focus();
});
})();
