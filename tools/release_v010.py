#!/usr/bin/env python3
"""Validate and export the reviewed v0.10 calibration release; reject unreviewed schema/data."""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
from build_core_v010 import SOURCES,PARENT,ARCHIVE
TABLES=['artifacts','taxa','experiments','code_objects','occurrences','edges','measurements','annotations','claims','claim_links','object_aliases','vocabulary','artifact_links','ingest_events','migration_audit']
EXPERIMENTS={'PC-0001','PC-0002','CAL-VOCAB','CAL-EXACTGAP','CAL-ORDERWIN','CAL-COMPRESS'}
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def validate(s,source_dir):
 require(s['source_database']['database_meta']['version']=='0.10','wrong core version')
 require(set(s['counts'])==set(TABLES),'unreviewed export table')
 for t in TABLES:
  require(len(s[t])==s['counts'][t],'count mismatch '+t)
  for row in s[t]:
   if 'evidence_tier' in row:require(row['evidence_tier']=='A','unreleased tier '+t)
 arts={r['artifact_id']:r for r in s['artifacts']};objs={r['object_id']:r for r in s['code_objects']}
 require(set(arts)=={'ART-PC0001','ART-PC0002','ART-VOCAB','ART-EXACTGAP','ART-ORDERWIN','ART-COMPRESS','ART-OLD-CODEBOOK'}|{v[0] for v in SOURCES.values()},'unreviewed artifact')
 require({r['experiment_id'] for r in s['experiments']}==EXPERIMENTS,'unreviewed experiment')
 for a in arts.values():require(a.get('exp0002_sensitive')==0,'sensitive or unclassified artifact')
 for t in TABLES:
  for row in s[t]:
   if 'source_artifact_id' in row:require(row['source_artifact_id'] in arts,'missing source '+t)
   if 'discovery_experiment_id' in row:require(row['discovery_experiment_id'] in EXPERIMENTS,'unreviewed discovery')
 for name,(aid,h) in SOURCES.items():require(sha((source_dir/name).read_bytes())==arts[aid]['sha256']==h,'source bytes mismatch '+name)
 for o in list(objs.values())+s['vocabulary']:
  if o.get('sequence'):
   seq=o['sequence'];require(len(seq)==o['length_bp'] and set(seq)<=set('ACGT') and sha(seq.encode())==o['sequence_sha256'],'sequence inconsistency')
 for o in s['occurrences']:
  require(o['object_id'] in objs,'dangling occurrence')
  require(o['start_0based']>=0 and o['end_0based_exclusive']-o['start_0based']==objs[o['object_id']]['length_bp'],'coordinate span')
  require(o['coordinate_basis']=='0-based half-open; direct input-record orientation' and o['strand']=='+','coordinate convention')
 for e in s['edges']:require(e['source_object_id'] in objs and e['target_object_id'] in objs,'dangling edge')
 for a in s['object_aliases']:require(a['canonical_object_id'] in objs and a['legacy_object_id'] not in objs,'broken alias')
 raw=json.loads((source_dir/'PC1_RAW_RECURRENCE_RESULTS.json').read_text())['focus_cluster']
 for key,oid in [('block_a','PC1-BLOCK-A25'),('block_b','PC1-BLOCK-B24'),('core_0001','PC1-CORE-16')]:require(objs[oid]['sequence']==raw[key],'raw identity mismatch')
 expected=set()
 for tax,kinds in raw['occurrences'].items():
  for kind,places in kinds.items():
   oid={'block_a':'PC1-BLOCK-A25','block_b':'PC1-BLOCK-B24','core':'PC1-CORE-16'}[kind]
   for rec,start in places:expected.add((oid,'TAX-'+tax,rec,start))
 require({(r['object_id'],r['taxon_id'],r['record_name'],r['start_0based']) for r in s['occurrences']}==expected and len(s['occurrences'])==19,'occurrence/source mismatch')
 metrics={r['measurement_id']:r for r in s['measurements']}
 require(metrics['PC1-M02']['value_num']==25 and metrics['PC1-M04']['value_num']==24,'A/B metrics')
 edges={r['edge_id']:r for r in s['edges']}
 require((edges['E-PC1-A-B']['source_object_id'],edges['E-PC1-A-B']['target_object_id'])==('PC1-BLOCK-A25','PC1-BLOCK-B24'),'A/B direction')
 require(edges['E-PC1-CONTAINS']['source_object_id']=='PC1-BLOCK-B24' and edges['E-PC1-CONTAINS']['exact_distance_bp']==4,'core containment')
 require(len(s['vocabulary'])==54 and len({r['sequence'] for r in s['vocabulary']})==54,'vocabulary inventory')
 frozen={r['sequence']:r for r in csv.DictReader((source_dir/'TRIPLE_SHARED_16MERS_COMPLETE.csv').open())}
 for v in s['vocabulary']:
  require(v['sequence'] in frozen,'unreviewed vocabulary')
  for col in ['ecoli_occurrences','pyro_occurrences','yeast_occurrences']:require(v[col]==int(frozen[v['sequence']][col]),'vocabulary count/source mismatch')
  require(v['entropy_bits']==float(frozen[v['sequence']]['entropy']),'vocabulary entropy/source mismatch')
 for link in s['artifact_links']:require(link['child_artifact_id'] in arts and link['parent_artifact_id'] in arts,'broken artifact path')
 require(len(s['ingest_events'])==1 and s['ingest_events'][0]['parent_database_sha256']==PARENT and s['ingest_events'][0]['archive_sha256']==ARCHIVE,'ingestion identity')
 require(all(r['event_id']==s['ingest_events'][0]['event_id'] for r in s['migration_audit']),'orphan audit')
 return {'sensitive_artifacts':0,'unreviewed_experiments':0,'invalid_sequences':0,'invalid_occurrences':0,'broken_provenance_links':0}
def export(db,root):
 c=sqlite3.connect(f'file:{db.resolve()}?mode=ro',uri=True);c.row_factory=sqlite3.Row
 require(not list(c.execute('PRAGMA foreign_key_check')),'foreign key violation')
 require(c.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity')
 require({r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}==set(TABLES)|{'meta'},'unreviewed table in database')
 s={t:[dict(r) for r in c.execute('SELECT * FROM '+t+' ORDER BY 1')] for t in TABLES}
 meta={r['key']:r['value'] for r in c.execute('SELECT * FROM meta')};c.close()
 s.update(snapshot_schema='LIFE_CODE_PUBLIC_SNAPSHOT_v0.10',generated_utc='2026-09-12T00:00:00Z',generation_time_semantics='Fixed release packaging epoch, not an experimental freeze or reveal time.',source_database={'filename':db.name,'sha256':sha(db.read_bytes()),'database_meta':meta})
 s['counts']={t:len(s[t]) for t in TABLES}
 checks=validate(s,root/'sources');s['public_release_gates']={'passed':True,'checks':checks,'rule':'Reviewed released calibration sources only. Primary EXP-0002 outcomes excluded. Legacy unknown source hashes remain explicit.'}
 out=root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.json';b=json.dumps(s,indent=2,ensure_ascii=False).encode();out.write_bytes(b)
 (root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.js').write_text('window.LIFE_CODE_SNAPSHOT='+json.dumps(s,separators=(',',':'),ensure_ascii=False)+';\n')
 (root/'data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.sha256').write_text(sha(b)+'  '+out.name+'\n')
 print(json.dumps({'sha256':sha(b),'counts':s['counts'],'gates':checks},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('database',type=Path);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();export(a.database,a.root)
