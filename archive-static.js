(()=>{'use strict';
const node=document.getElementById('archive-data');if(!node)return;
const data=JSON.parse(node.textContent),box=document.getElementById('records'),q=document.getElementById('q'),sort=document.getElementById('sort'),count=document.getElementById('count');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function href(value){try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password?esc(u.href):''}catch{return ''}}
function render(){let rows=data.filter(r=>[r.date,r.title,r.kind,r.desc,r.dir].join(' ').toLowerCase().includes(q.value.trim().toLowerCase()));
if(sort.value==='date-desc')rows.sort((a,b)=>b.date.localeCompare(a.date)||a.title.localeCompare(b.title));
if(sort.value==='date-asc')rows.sort((a,b)=>a.date.localeCompare(b.date)||a.title.localeCompare(b.title));
if(sort.value==='title')rows.sort((a,b)=>a.title.localeCompare(b.title,'ko'));
count.textContent=rows.length+'개';box.innerHTML=rows.map(r=>'<article class="record"><time>'+esc(r.date)+'</time><small>'+esc(r.kind)+(r.dir&&href(r.repoUrl)?' · <a class="record-dir" href="'+href(r.repoUrl)+'"><code>'+esc(r.dir)+'</code></a>':'')+'</small><h3><a class="record-title" href="'+href(r.url)+'">'+esc(r.title)+'</a></h3><p>'+esc(r.desc)+'</p><a class="open" href="'+href(r.url)+'">상세 기록 열기 →</a></article>').join('')}
q.addEventListener('input',render);sort.addEventListener('change',render);document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{box.className='records '+b.dataset.view}));render();
})();
