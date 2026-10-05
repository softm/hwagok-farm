#!/usr/bin/env python3
"""Stop public publication when metadata declares private or sensitive material."""
import json, sys, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORDS=('비공개','농지증여','경영체','보험','진료','의료','계약서')
def inspect(root=ROOT):
 held=[]
 for folder in sorted((root/'public/records').glob('*')):
  if not folder.is_dir(): continue
  for name in ('archive.json','archive-manifest.json'):
   path=folder/name
   if not path.is_file(): continue
   data=json.loads(path.read_text(encoding='utf-8'))
   nested=data.get('metadata',{}) or {}
   text=' '.join(str(x) for x in (data.get('source',''),data.get('title',''),nested.get('title','')))
   visibility=nested.get('visibility',data.get('visibility','public'))
   if visibility!='public' or any(w in unicodedata.normalize('NFC',text) for w in WORDS):
    held.append({'record':folder.name,'reason':'private-or-sensitive-metadata'});break
 result={'passed':not held,'held':held}
 out=root/'.archive-run/public-scope.json';out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 result=inspect();print(json.dumps(result,ensure_ascii=False))
 if not result['passed']: raise SystemExit('Public deployment held. Move/review sensitive records under the existing private-archive policy before publishing. No sources were deleted.')
