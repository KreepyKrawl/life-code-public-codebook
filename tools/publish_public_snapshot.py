#!/usr/bin/env python3
"""Generate a public LIFE-CODE snapshot from the local canonical SQLite Codebook.

Hard gates:
- blocks export if any artifact is marked exp0002_sensitive=1
- blocks export if any Tier-C object, measurement, edge, or claim is present
- exports data only; presentation reads the generated snapshot
"""
from pathlib import Path
import sqlite3,json,hashlib,datetime,argparse

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def rows(c,q):
    return [dict(r) for r in c.execute(q).fetchall()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("database")
    ap.add_argument("output")
    a=ap.parse_args()
    c=sqlite3.connect(a.database);c.row_factory=sqlite3.Row
    checks={
      "exp0002_sensitive_artifacts":c.execute("SELECT COUNT(*) n FROM artifacts WHERE exp0002_sensitive=1").fetchone()["n"],
      "tier_c_objects":c.execute("SELECT COUNT(*) n FROM code_objects WHERE evidence_tier='C'").fetchone()["n"],
      "tier_c_edges":c.execute("SELECT COUNT(*) n FROM edges WHERE evidence_tier='C'").fetchone()["n"],
      "tier_c_measurements":c.execute("SELECT COUNT(*) n FROM measurements WHERE evidence_tier='C'").fetchone()["n"],
      "tier_c_claims":c.execute("SELECT COUNT(*) n FROM claims WHERE evidence_tier='C'").fetchone()["n"],
    }
    if any(checks.values()):
        raise SystemExit("PUBLIC EXPORT BLOCKED: "+json.dumps(checks))
    tabs=["taxa","experiments","occurrences","annotations","claim_links"]
    s={
      "snapshot_schema":"LIFE_CODE_PUBLIC_SNAPSHOT_v0.9",
      "generated_utc":datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
      "source_database":{"filename":Path(a.database).name,"sha256":sha(a.database),
                         "database_meta":{r["key"]:r["value"] for r in c.execute("SELECT key,value FROM meta")}},
      "public_release_gates":{"passed":True,"checks":checks,
        "rule":"No EXP-0002-sensitive artifacts and no Tier-C scientific records may enter this public snapshot."},
      "artifacts":rows(c,"SELECT artifact_id,name,role,sha256,authority_level,source_status,notes FROM artifacts WHERE exp0002_sensitive=0 ORDER BY artifact_id"),
      "code_objects":rows(c,"SELECT * FROM code_objects WHERE evidence_tier!='C' ORDER BY object_type,object_id"),
      "edges":rows(c,"SELECT * FROM edges WHERE evidence_tier!='C' ORDER BY source_object_id,edge_type,target_object_id"),
      "measurements":rows(c,"SELECT * FROM measurements WHERE evidence_tier!='C' ORDER BY subject_type,subject_id,measurement_id"),
      "claims":rows(c,"SELECT * FROM claims WHERE evidence_tier!='C' ORDER BY claim_id")}
    for t in tabs:s[t]=rows(c,f"SELECT * FROM {t}")
    s["counts"]={k:len(v) for k,v in s.items() if isinstance(v,list)}
    c.close()
    out=Path(a.output);out.write_text(json.dumps(s,indent=2,ensure_ascii=False),encoding="utf-8")
    print(out)
    print("sha256",sha(out))
if __name__=="__main__":main()
