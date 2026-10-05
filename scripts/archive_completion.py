#!/usr/bin/env python3
"""Policy check, central metadata synchronization and fail-closed inbox cleanup."""
from __future__ import annotations
import base64, json, os, shutil, subprocess, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from archive_inbox import ROOT, REPO, POLICY, digest, fingerprint, jwrite, relpath, verify_files

RUN=ROOT/'.archive-run'
CENTRAL_REPO='softm/softm.github.io'


def api(path, token='', method='GET', data=None):
 headers={'Accept':'application/vnd.github+json','User-Agent':'SOFTM-Archive-Completion','X-GitHub-Api-Version':'2022-11-28'}
 if token: headers['Authorization']='Bearer '+token
 body=None if data is None else json.dumps(data,ensure_ascii=False).encode()
 if body: headers['Content-Type']='application/json'
 with urlopen(Request('https://api.github.com/'+quote(path,safe='/?:=&%'),data=body,headers=headers,method=method),timeout=45) as response:
  raw=response.read();return json.loads(raw) if raw else {}

def load_plan(): return json.loads((RUN/'plan.json').read_text(encoding='utf-8'))

def proof_base(plan):
 return {'planHash':digest(RUN/'plan.json'),'sourceSha':plan['sourceSha'],'runId':os.getenv('GITHUB_RUN_ID','local'),'runAttempt':os.getenv('GITHUB_RUN_ATTEMPT','1')}

def policy():
 # A newer unreviewed policy must not silently be reported as implemented.
 results={}
 for path,expected in POLICY.items():
  doc=api('repos/'+CENTRAL_REPO+'/contents/'+path+'?ref=main')
  results[path]=doc['sha']
  if doc['sha']!=expected: raise RuntimeError('Archive policy changed; review implementation before publication: '+path)
 jwrite(RUN/'policy.json',{'verified':True,'blobs':results})

def stamp():
 plan=load_plan();plan['sourceSha']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 jwrite(RUN/'plan.json',plan)

def read_proof(name,plan):
 p=json.loads((RUN/name).read_text(encoding='utf-8'))
 if not p.get('passed') or any(p.get(k)!=v for k,v in proof_base(plan).items()):
  raise RuntimeError('Missing, failed or stale completion evidence: '+name)
 return p

def central():
 plan=load_plan();read_proof('live.json',plan)
 document=api('repos/'+CENTRAL_REPO+'/contents/projects/projects.json?ref=main')
 data=json.loads(base64.b64decode(document['content']))
 project=next(p for p in data['projects'] if p['repo']=='hwagok-farm')
 by_url={item['url']:item for item in project.get('links',[])}
 changed=False
 for record in plan['records']:
  m=record['metadata']; entry={k:m[k] for k in ('id','title','userTitle','date','authoredAt','dateSource','url','repoUrl','directory','recordPath','category','summary','visibility')}
  entry.update(label=m['title'],chatTitle=m['title'])
  old=by_url.get(m['url'],{})
  if any(old.get(k)!=v for k,v in entry.items()): changed=True
  by_url[m['url']]={**old,**entry}
 project['links']=list(by_url.values())
 project['homePublicListCount']=sum(x.get('visibility')=='public' for x in project['links'])
 project['pageCount']=project['homePublicListCount']
 jwrite(RUN/'central-proposal.json',data)
 if changed:
  token=os.getenv('ARCHIVE_INDEX_TOKEN','')
  if not token:
   raise RuntimeError('Central index needs updates. Configure ARCHIVE_INDEX_TOKEN for softm/softm.github.io Contents + Actions write, or apply central-proposal.json there. Inbox is retained.')
  result=api('repos/'+CENTRAL_REPO+'/contents/projects/projects.json',token,'PUT',{'sha':document['sha'],'branch':'main','message':'archive: synchronize verified hwagok inbox record metadata','content':base64.b64encode((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()).decode()})
  api('repos/'+CENTRAL_REPO+'/actions/workflows/publish-project-homes.yml/dispatches',token,'POST',{'ref':'main'})
  commit=result['commit']['sha']
 else: commit=document['sha']
 jwrite(RUN/'index-sync.json',{**proof_base(plan),'passed':True,'centralRevision':commit,'changed':changed,'publicCount':project['homePublicListCount']})

def check_cleanup(root: Path, plan, proof):
 if not proof.get('passed') or proof.get('sourceSha')!=plan.get('sourceSha'): raise RuntimeError('Final verification required')
 expected={'detail','service-home','central-home','top-index','media','original-bytes','source-directory-links','title-parity'}
 if set(proof.get('checks',[]))!=expected: raise RuntimeError('Incomplete final verification gates')
 if set(proof.get('slugs',[]))!={r['slug'] for r in plan['records']}: raise RuntimeError('Wrong record verification set')
 for task in plan['records']:
  p=relpath(task['input'])
  if len(p.parts)!=2 or p.parts[0]!='zip': raise RuntimeError('Cleanup escaped inbox unit')
  source=root/p
  if not source.exists() or fingerprint(source)!=task['inputHash']: raise RuntimeError('Input changed since build; preserve it')
  dest=relpath(task['recordPath'])
  if len(dest.parts)!=3 or dest.parts[:2]!=('public','records'): raise RuntimeError('Invalid final record path')
  verify_files(root/dest,task['files'])

def cleanup():
 if os.getenv('GITHUB_ACTIONS')!='true' or os.getenv('GITHUB_REF')!='refs/heads/main': raise RuntimeError('Cleanup runs only in the trusted main workflow')
 plan=load_plan();read_proof('index-sync.json',plan);proof=read_proof('final.json',plan)
 if not plan['records']: return
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if head!=plan['sourceSha']: raise RuntimeError('Source revision changed')
 subprocess.run(['git','fetch','origin','main'],cwd=ROOT,check=True)
 remote=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
 if remote!=head: raise RuntimeError('Concurrent upload detected; cleanup deferred')
 check_cleanup(ROOT,plan,proof)
 receipt={**proof,'inputs':[{'path':r['input'],'sha256':r['inputHash'],'recordPath':r['recordPath']} for r in plan['records']]}
 ledger=ROOT/'.archive-ledger'/('run-'+os.environ['GITHUB_RUN_ID']+'-'+os.getenv('GITHUB_RUN_ATTEMPT','1')+'.json')
 jwrite(ledger,receipt)
 for task in plan['records']:
  p=ROOT/task['input']
  if p.is_dir(): shutil.rmtree(p)
  else: p.unlink()
 paths=[t['input'] for t in plan['records']]+[ledger.relative_to(ROOT).as_posix()]
 subprocess.run(['git','add','--all','--',*paths],cwd=ROOT,check=True)
 subprocess.run(['git','commit','-m','archive: clean only live-verified inbox inputs'],cwd=ROOT,check=True)
 # A normal push rejects a concurrent writer; no force or reset is used.
 subprocess.run(['git','push','origin','HEAD:main'],cwd=ROOT,check=True)

if __name__=='__main__':
 commands={'policy':policy,'stamp':stamp,'sync':central,'cleanup':cleanup}
 if len(sys.argv)!=2 or sys.argv[1] not in commands: raise SystemExit('policy | stamp | sync | cleanup')
 commands[sys.argv[1]]()
