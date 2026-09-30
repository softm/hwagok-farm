/** Build list/detail labels from the existing central title policy; retain all record bodies/assets. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const ts = require('typescript');
const root = process.cwd();
const report = {version:'20260930-compact-detail-v1', normalized:[], missing:[], titlePolicy:'projects/project-home.js', mediaUnchanged:false};
const base = process.env.GITHUB_ACTIONS === 'true' ? '/hwagok-farm' : '';
const local = p => { const result=path.resolve(root,p); if (!result.startsWith(root+path.sep)) throw new Error('Path outside repository: '+p); return result; };
const read = p => fs.readFileSync(local(p),'utf8');
const write = (p,s) => { fs.mkdirSync(path.dirname(local(p)),{recursive:true}); fs.writeFileSync(local(p),s); };
const hashAssets = dir => {
  const items=[];
  function walk(d) { if (!fs.existsSync(d)) return; for (const e of fs.readdirSync(d,{withFileTypes:true})) { const p=path.join(d,e.name); if (e.isDirectory()) walk(p); else if (/\.(?:jpe?g|png|webp|gif|svg|mp4|mov|m4a|mp3|wav|pdf|zip)$/i.test(e.name)) items.push(p+':'+crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')); } }
  walk(local(dir)); return crypto.createHash('sha256').update(items.sort().join('\n')).digest('hex');
};
const assetsBefore = hashAssets('public');
async function get(url) {
  for(let attempt=0;attempt<3;attempt++) { try { const r=await fetch(url,{signal:AbortSignal.timeout(30000)}); if(!r.ok)throw new Error(`${r.status} ${url}`); return await r.text(); } catch(error) { if(attempt===2)throw error; await new Promise(r=>setTimeout(r,1000*(attempt+1))); } }
}
let inputs;
if(process.env.DETAIL_TITLE_INPUT) inputs=JSON.parse(fs.readFileSync(process.env.DETAIL_TITLE_INPUT,'utf8'));
else {
  const head=JSON.parse(await get('https://api.github.com/repos/softm/softm.github.io/git/ref/heads/main')).object.sha;
  const prefix=`https://raw.githubusercontent.com/softm/softm.github.io/${head}/projects/`;
  const [catalogText,metadataText,policy]=await Promise.all(['projects.json','chat-metadata.json','project-home.js'].map(p=>get(prefix+p)));
  inputs={revision:head,catalog:JSON.parse(catalogText),metadata:JSON.parse(metadataText),policy};
}
if(inputs.metadata.schemaVersion!==1||!inputs.metadata.entries) throw new Error('Invalid central title metadata');
const context={module:{exports:{}},URL,Intl,Date,Set,Map};
vm.runInNewContext(inputs.policy,context,{timeout:3000});
const policy=context.module.exports;
if(typeof policy.display!=='function'||typeof policy.lists!=='function') throw new Error('Central title policy exports changed');
const project=inputs.catalog.projects.find(p=>p.repo==='hwagok-farm');
if(!project) throw new Error('Missing hwagok-farm in projects registry');
const rows=policy.lists(project,inputs.metadata).public;
const byURL=new Map(rows.map(row=>[policy.keyFor(row.url),row]));
const source=read('archive/records.ts');
const compiled=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020}}).outputText;
const recordsContext={exports:{}};
vm.runInNewContext(compiled,recordsContext,{timeout:3000});
const records=recordsContext.exports.archiveRecords;
if(!Array.isArray(records)||!records.length)throw new Error('Missing archive records');
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalized = records.map(r=>{
  const originalArchiveTitle=r.originalArchiveTitle||r.title;
  const urls=[`https://softm.github.io/hwagok-farm${r.legacyPath}`,`https://softm.github.io/hwagok-farm/archive/${r.slug}/`];
  const found=urls.map(u=>byURL.get(policy.keyFor(u))).find(Boolean);
  const metadata=urls.map(u=>inputs.metadata.entries[policy.keyFor(u)]).find(Boolean)||{};
  const label=found||policy.display({...metadata,title:originalArchiveTitle});
  return {...r,originalArchiveTitle,title:label.displayTitle,displayName:label.displayName,displayDate:label.displayDate};
});
const normalizedType='export type ArchiveRecord = {slug:string;kind:string;title:string;description:string;meta:string[];legacyPath:string;assets:null|{md?:string;html?:string;zip?:string};assetStatus:string;displayName?:string;displayDate?:string;originalArchiveTitle?:string;[key:string]:unknown};\n';
write('archive/records.ts',normalizedType+'export const archiveRecords: ArchiveRecord[] = '+JSON.stringify(normalized,null,2)+';\n');
function jsxTitle(r) { return '<h1 data-record-title><span className="record-date">{'+JSON.stringify(r.displayDate||'작성일 미확인')+'}</span>{" "}<span>{'+JSON.stringify(r.displayName)+'}</span></h1>'; }
function htmlTitle(r) { return '<h1 data-record-title><span class="record-date">'+escape(r.displayDate||'작성일 미확인')+'</span> <span>'+escape(r.displayName)+'</span></h1>'; }
function patchTSX(file,r) {
  let text=read(file);
  const ast=ts.createSourceFile(file,text,ts.ScriptTarget.Latest,true,ts.ScriptKind.TSX);
  const titles=[];
  function visit(n) { if(ts.isJsxElement(n)&&n.openingElement.tagName.getText(ast)==='h1') titles.push(n); ts.forEachChild(n,visit); }
  visit(ast);
  if(titles.length!==1) { report.missing.push({file,reason:`Expected one h1; found ${titles.length}`});return false; }
  const n=titles[0];text=text.slice(0,n.getStart(ast))+jsxTitle(r)+text.slice(n.end);
  const client=/^[\s\n]*(?:\/\*[\s\S]*?\*\/\s*)?["']use client["']/.test(text);
  if(!client&&!/export\s+(?:const\s+metadata|(?:async\s+)?function\s+generateMetadata)/.test(text)) text+='\nexport const metadata = {title: '+JSON.stringify(r.title+' · 화곡농장')+'};\n';
  write(file,text);report.normalized.push({file,slug:r.slug,title:r.title,kind:'react'});return true;
}
function patchHTML(file,r) {
  if(!fs.existsSync(local(file))) return false;
  let text=read(file);
  if(!/<h1\b/i.test(text))return false;
  text=text.replace(/<h1\b[^>]*>[\s\S]*?<\/h1>/i,htmlTitle(r));
  text=text.replace(/<title\b[^>]*>[\s\S]*?<\/title>/i,'<title>'+escape(r.title+' · 화곡농장')+'</title>');
  if(!/<html\b[^>]*data-record-detail/i.test(text))text=text.replace(/<html\b/i,'<html data-record-detail="compact-v1"');
  if(!/data-record-page/.test(text))text=text.replace(/<main\b/i,'<main data-record-page');
  const additions=`<link rel="stylesheet" href="${base}/archive-detail.css?v=20260930-compact-v1"><script defer src="${base}/archive-detail.js?v=20260930-compact-v1"></script>`;
  if(!text.includes('archive-detail.css'))text=text.replace(/<\/head>/i,additions+'\n</head>');
  write(file,text);report.normalized.push({file,slug:r.slug,title:r.title,kind:'html'});return true;
}
for(const r of normalized) {
  const route=r.legacyPath.split(/[?#]/)[0].replace(/^\/+|\/+$/g,'');
  let found=false;
  const page='app/'+route.replace(/\/index\.html$/,'')+'/page.tsx';
  if(fs.existsSync(local(page)))found=patchTSX(page,r);
  const raw='public/'+route+(/\.html$/i.test(route)?'':'/index.html');
  if(fs.existsSync(local(raw)))found=patchHTML(raw,r)||found;
  if(r.assets?.html)patchHTML('public/'+r.assets.html.replace(/^\//,''),r);
  if(!found)report.missing.push({slug:r.slug,route:r.legacyPath,reason:'No direct route file; may be a generated redirect'});
}
let layout=read('app/layout.tsx');
if(!layout.includes('archive-detail.css'))layout=layout.replace('import "./globals.css";','import "./globals.css";\nimport "../public/archive-detail.css";\nimport DetailEnhancer from "./DetailEnhancer";');
if(!layout.includes('<DetailEnhancer'))layout=layout.replace('</body>','<DetailEnhancer /></body>');
write('app/layout.tsx',layout);
report.centralRevision=inputs.revision;
report.recordCount=normalized.length;
report.records=normalized.map(r=>({slug:r.slug,legacyPath:r.legacyPath,title:r.title,name:r.displayName,date:r.displayDate}));
report.mediaUnchanged=assetsBefore===hashAssets('public');
if(!report.mediaUnchanged)throw new Error('A binary media asset changed while applying detail layout');
write('public/detail-ui-report.json',JSON.stringify(report,null,2)+'\n');
console.log(`Detail UI: ${report.normalized.length} documents, ${normalized.length} records, all binary media unchanged.`);
for(const item of report.missing)console.warn('CHECK',JSON.stringify(item));
