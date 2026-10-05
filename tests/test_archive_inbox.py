import base64, copy, json, os, stat, sys, tempfile, unittest, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from archive_inbox import build, build_batch, digest, fingerprint, inventory, jwrite, relpath, unpack, verify_files
from archive_completion import check_cleanup
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jH+YAAAAASUVORK5CYII=')
DOC='# 작업 기록\n\n첫 번째 상세 문단입니다.\n\n## 상세 작업\n\n누락되면 안 되는 마지막 문단입니다.\n\n![사진](사진.png)\n'
CHECKS=['detail','service-home','central-home','top-index','media','original-bytes','source-directory-links','title-parity']

class InboxTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'zip').mkdir()
  (self.root/'index.html').write_text('<html><script id="archive-data" type="application/json">[]</script></html>')
 def tearDown(self): self.tmp.cleanup()
 def zip(self,name='20261005_test.zip',files=None):
  p=self.root/'zip'/name
  with zipfile.ZipFile(p,'w') as z:
   for name,data in (files or {'note.md':DOC,'사진.png':PNG}).items():z.writestr(name,data)
  return p
 def test_full_narrative_and_original_preserved(self):
  p=self.zip();before=p.read_bytes();r=build(p,self.root);target=self.root/r['recordPath']
  self.assertIn('누락되면 안 되는 마지막 문단',(target/'index.html').read_text())
  self.assertIn('누락되면 안 되는 마지막 문단',(target/'summary.md').read_text())
  self.assertEqual((target/'source/note.md').read_text(),DOC)
  self.assertEqual((target/'source/사진.png').read_bytes(),PNG)
  self.assertEqual(p.read_bytes(),before);verify_files(target,r['files'])
 def test_nested_single_directory(self):
  p=self.zip(files={'outer/inner/note.md':DOC,'outer/inner/사진.png':PNG})
  r=build(p,self.root);self.assertTrue((self.root/r['recordPath']/'source/사진.png').is_file())
 def test_full_html_preserved_and_title_shared(self):
  raw='<html><head><title>Old</title></head><body><h1>일지</h1><p>세부 원문</p></body></html>'
  p=self.zip(files={'index.html':raw});r=build(p,self.root);target=self.root/r['recordPath']
  self.assertEqual((target/'source/index.html').read_text(),raw)
  self.assertIn(r['metadata']['title'],(target/'index.html').read_text());self.assertIn('세부 원문',(target/'summary.md').read_text())
 def test_folder_hash_changes(self):
  d=self.root/'zip/20261005_folder';d.mkdir();(d/'note.md').write_text(DOC);(d/'사진.png').write_bytes(PNG)
  before=fingerprint(d);(d/'note.md').write_text(DOC+'new text');self.assertNotEqual(before,fingerprint(d))
 def test_folder_supported_and_not_deleted(self):
  d=self.root/'zip/20261005_folder';d.mkdir();(d/'note.md').write_text(DOC);(d/'사진.png').write_bytes(PNG)
  r=build(d,self.root);self.assertTrue(d.is_dir());self.assertEqual(r['inputHash'],fingerprint(d))
 def test_repeated_exact_zip_keeps_canonical_slug(self):
  p=self.zip();first=build(p,self.root);second=build(p,self.root)
  self.assertEqual(first['slug'],second['slug']);self.assertTrue(second['reused']);self.assertTrue(p.exists())
 def test_changed_folder_is_not_none_equals_none(self):
  d=self.root/'zip/20261005_folder';d.mkdir();(d/'note.md').write_text(DOC);(d/'사진.png').write_bytes(PNG)
  first=build(d,self.root);(d/'note.md').write_text(DOC+' changed')
  with self.assertRaisesRegex(ValueError,'already exists'):build(d,self.root)
  self.assertTrue(d.exists());self.assertEqual((self.root/first['recordPath']/'source/note.md').read_text(),DOC)
 def test_corrupt_existing_output_is_not_skipped(self):
  p=self.zip();r=build(p,self.root);(self.root/r['recordPath']/'source/사진.png').unlink()
  with self.assertRaisesRegex(ValueError,'Missing/changed'):build(p,self.root)
  self.assertTrue(p.exists())
 def test_date_range_and_heading_whitespace(self):
  p=self.zip(name='20260701-0702_repair.zip',files={'note.md':'# 2026-07-01~02 냉동고 수리\n기록\n\n상세 원문'})
  r=build(p,self.root)
  self.assertEqual(r['metadata']['dateEnd'],'2026-07-02')
  self.assertNotIn('2026-07-01 2026-',r['metadata']['title'])
  self.assertNotIn('\n',r['metadata']['title'])
 def test_zip_traversal_rejected(self):
  p=self.zip(files={'../escape.txt':'bad'})
  with self.assertRaises(ValueError):build(p,self.root)
  self.assertFalse((self.root/'escape.txt').exists());self.assertTrue(p.exists())
 def test_symlink_zip_rejected(self):
  p=self.root/'zip/20261005_link.zip'
  with zipfile.ZipFile(p,'w') as z:
   i=zipfile.ZipInfo('bad');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,'/etc/passwd')
  with self.assertRaises(ValueError):build(p,self.root)
 def test_unicode_collision_rejected(self):
  p=self.zip(files={'가.txt':'a','가.txt':'b'})
  with self.assertRaisesRegex(ValueError,'Duplicate'):build(p,self.root)
 def test_mac_metadata_ignored(self):
  p=self.zip(files={'note.md':DOC,'사진.png':PNG,'__MACOSX/._note.md':'junk','.DS_Store':'junk'})
  r=build(p,self.root);self.assertFalse(any('__MACOSX' in x['path'] for x in r['files']))
 def test_undated_input_is_held(self):
  p=self.zip(name='unknown.zip')
  with self.assertRaisesRegex(ValueError,'date'):build(p,self.root)
 def test_private_metadata_is_held(self):
  p=self.zip(files={'archive.json':json.dumps({'visibility':'private'}),'note.md':DOC})
  with self.assertRaisesRegex(ValueError,'Private'):build(p,self.root)
 def test_sensitive_filename_is_held(self):
  p=self.zip(name='20261005_경영체.zip')
  with self.assertRaisesRegex(ValueError,'sensitive'):build(p,self.root)
 def test_no_filename_only_html(self):
  p=self.zip(files={'사진.png':PNG})
  with self.assertRaisesRegex(ValueError,'No narrative'):build(p,self.root)
 def test_cleanup_requires_all_gates(self):
  p=self.zip();r=build(p,self.root);plan={'sourceSha':'abc','records':[r]}
  with self.assertRaises(RuntimeError):check_cleanup(self.root,plan,{'passed':True,'sourceSha':'abc','checks':['detail'],'slugs':[r['slug']]})
  self.assertTrue(p.exists())
 def test_cleanup_rejects_changed_upload(self):
  p=self.zip();r=build(p,self.root);plan={'sourceSha':'abc','records':[r]};p.write_bytes(p.read_bytes()+b'changed')
  with self.assertRaisesRegex(RuntimeError,'Input changed'):check_cleanup(self.root,plan,{'passed':True,'sourceSha':'abc','checks':CHECKS,'slugs':[r['slug']]})
 def test_cleanup_proof_can_validate_without_deleting(self):
  p=self.zip();r=build(p,self.root);plan={'sourceSha':'abc','records':[r]}
  check_cleanup(self.root,plan,{'passed':True,'sourceSha':'abc','checks':CHECKS,'slugs':[r['slug']]});self.assertTrue(p.exists())
 def test_cleanup_cannot_escape_inbox(self):
  p=self.zip();r=build(p,self.root);r['input']='public/records';plan={'sourceSha':'abc','records':[r]}
  with self.assertRaises(RuntimeError):check_cleanup(self.root,plan,{'passed':True,'sourceSha':'abc','checks':CHECKS,'slugs':[r['slug']]})
 def test_empty_inbox_has_no_completion_claim(self):
  plan=build_batch(self.root);self.assertEqual(plan['records'],[]);self.assertFalse((self.root/'.archive-run/final.json').exists())
 def test_service_home_uses_same_record_metadata(self):
  self.zip();plan=build_batch(self.root);text=(self.root/'index.html').read_text()
  self.assertIn(plan['records'][0]['metadata']['title'],text)
  self.assertTrue((self.root/'zip/20261005_test.zip').exists())
if __name__=='__main__':unittest.main()
