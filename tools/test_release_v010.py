#!/usr/bin/env python3
"""Regression gates for recovered scientific identity, leakage, and preserved history."""
import copy,json,sqlite3,sys,tempfile,hashlib
from pathlib import Path
from release_v010 import validate
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from lifecode_codebook import connect,object_payload,export_all
s=json.loads((R/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.json').read_text());validate(s,R/'sources')
def rejects(label,change):
 x=copy.deepcopy(s);change(x)
 try:validate(x,R/'sources')
 except (ValueError,KeyError):print('PASS reject',label);return
 raise AssertionError('Gate accepted '+label)
rejects('sensitive source',lambda x:x['artifacts'][0].update(exp0002_sensitive=1))
rejects('Tier C measurement',lambda x:x['measurements'][0].update(evidence_tier='C'))
rejects('unreviewed experiment',lambda x:x['experiments'][0].update(experiment_id='EXP-0002'))
rejects('wrong A/B length metric',lambda x:next(r for r in x['measurements'] if r['measurement_id']=='PC1-M02').update(value_num=24))
rejects('wrong coordinate',lambda x:x['occurrences'][0].update(start_0based=x['occurrences'][0]['start_0based']+1))
rejects('wrong vocabulary count',lambda x:x['vocabulary'][0].update(ecoli_occurrences=999))
rejects('dangling alias',lambda x:x['object_aliases'][0].update(canonical_object_id='MISSING'))
js=(R/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.js').read_text();assert json.loads(js.split('=',1)[1].strip().rstrip(';'))==s
c=connect(R/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite')
assert object_payload(c,'PC1-BLOCK-A24')['object']['object_id']=='PC1-BLOCK-B24'
assert len(export_all(c)['vocabulary'])==54
for table in ['migration_audit','ingest_events']:
 try:c.execute('DELETE FROM '+table)
 except sqlite3.IntegrityError:pass
 else:raise AssertionError('Audit mutable')
c.close()
old=connect(R/'LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite');assert object_payload(old,'PC1-BLOCK-A24')['object']['sequence'] is None;assert len(export_all(old)['measurements'])==190;old.close()
assert hashlib.sha256((R/'LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite').read_bytes()).hexdigest()=='63910fdf80df38e543cb3b755c60cd3ce146e58140ab7fae9e051153b05b93bb'
# Every original row is retained or its exact before/after state is auditable.
p=connect(R/'LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite');q=connect(R/'downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite')
audit={(r['table_name'],r['record_id']):dict(r) for r in q.execute('SELECT * FROM migration_audit')}
for table in ['meta','artifacts','taxa','experiments','code_objects','occurrences','edges','measurements','annotations','claims','claim_links']:
 before={str(r[0]):dict(r) for r in p.execute('SELECT * FROM '+table)};after={str(r[0]):dict(r) for r in q.execute('SELECT * FROM '+table)}
 for key in before.keys()|after.keys():
  if before.get(key)!=after.get(key):
   a=audit[(table,key)];assert json.loads(a['before_json'] or 'null')==before.get(key);assert json.loads(a['after_json'] or 'null')==after.get(key)
p.close();q.close()
print('PASS snapshot equality, legacy CLI, append-only audit, source preservation, complete before/after audit')
