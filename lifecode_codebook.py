#!/usr/bin/env python3
"""LIFE-CODE Codebook Core v0.8 — executable SQLite CLI.

Standard-library only. The supplied database contains released Tier-A
calibration evidence and no EXP-0002 outcome values.
"""
from __future__ import annotations
import argparse,json,sqlite3,pathlib,hashlib

HERE=pathlib.Path(__file__).resolve().parent
DEFAULT_DB=HERE/"LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite"

def connect(db):
    con=sqlite3.connect(db)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def rows(cur):
    return [dict(r) for r in cur.fetchall()]

def object_payload(con,oid):
    obj=con.execute("SELECT * FROM code_objects WHERE object_id=?",(oid,)).fetchone()
    if not obj:return None
    aid=obj["source_artifact_id"]
    art=con.execute("SELECT * FROM artifacts WHERE artifact_id=?",(aid,)).fetchone() if aid else None
    return {
      "object":dict(obj),
      "edges_out":rows(con.execute("SELECT * FROM edges WHERE source_object_id=? ORDER BY edge_type,target_object_id",(oid,))),
      "edges_in":rows(con.execute("SELECT * FROM edges WHERE target_object_id=? ORDER BY edge_type,source_object_id",(oid,))),
      "occurrences":rows(con.execute("SELECT * FROM occurrences WHERE object_id=? ORDER BY taxon_id,start_0based",(oid,))),
      "measurements":rows(con.execute("SELECT * FROM measurements WHERE subject_type='OBJECT' AND subject_id=? ORDER BY measurement_id",(oid,))),
      "annotations":rows(con.execute("SELECT * FROM annotations WHERE subject_type='OBJECT' AND subject_id=? ORDER BY annotation_type",(oid,))),
      "artifact":dict(art) if art else None
    }

def experiment_payload(con,eid):
    e=con.execute("SELECT * FROM experiments WHERE experiment_id=?",(eid,)).fetchone()
    if not e:return None
    return {
      "experiment":dict(e),
      "objects":rows(con.execute("SELECT * FROM code_objects WHERE discovery_experiment_id=? ORDER BY object_type,object_id",(eid,))),
      "measurements":rows(con.execute("SELECT * FROM measurements WHERE subject_type='EXPERIMENT' AND subject_id=? ORDER BY measurement_id",(eid,))),
      "annotations":rows(con.execute("SELECT * FROM annotations WHERE subject_type='EXPERIMENT' AND subject_id=? ORDER BY annotation_type",(eid,)))
    }

def stats(con):
    return {
      "database":{r["key"]:r["value"] for r in con.execute("SELECT * FROM meta")},
      "counts":{t:con.execute(f"SELECT COUNT(*) n FROM {t}").fetchone()["n"] for t in
                ["artifacts","experiments","code_objects","edges","measurements","annotations","claims"]},
      "objects_by_type":rows(con.execute("SELECT object_type,COUNT(*) n FROM code_objects GROUP BY object_type ORDER BY object_type")),
      "objects_by_evidence_state":rows(con.execute("SELECT evidence_state,COUNT(*) n FROM code_objects GROUP BY evidence_state ORDER BY evidence_state"))
    }

def verify(con):
    issues=[]
    fk=list(con.execute("PRAGMA foreign_key_check"))
    if fk:issues.append({"type":"foreign_key","rows":[tuple(x) for x in fk]})
    tierc={}
    for t in ["code_objects","measurements","claims"]:
        tierc[t]=con.execute(f"SELECT COUNT(*) n FROM {t} WHERE evidence_tier='C'").fetchone()["n"]
    if any(tierc.values()):issues.append({"type":"tier_c_present","counts":tierc})
    n=con.execute("SELECT COUNT(*) n FROM artifacts WHERE exp0002_sensitive=1").fetchone()["n"]
    if n:issues.append({"type":"exp0002_sensitive_artifacts_present","count":n})
    bad=[]
    for r in con.execute("SELECT artifact_id,sha256 FROM artifacts WHERE sha256 IS NOT NULL"):
        s=r["sha256"]
        if len(s)!=64 or any(c not in "0123456789abcdef" for c in s.lower()):bad.append(dict(r))
    if bad:issues.append({"type":"bad_sha256","rows":bad})
    seqbad=[]
    for r in con.execute("SELECT object_id,sequence,sequence_sha256 FROM code_objects WHERE sequence IS NOT NULL"):
        calc=hashlib.sha256(r["sequence"].encode()).hexdigest()
        if calc!=r["sequence_sha256"]:seqbad.append({"object_id":r["object_id"],"stored":r["sequence_sha256"],"calculated":calc})
    if seqbad:issues.append({"type":"sequence_hash_mismatch","rows":seqbad})
    missing=rows(con.execute("SELECT object_id,label,data_completeness FROM code_objects WHERE data_completeness LIKE '%NOT_RECOVERED%'"))
    return {"ok":not issues,"issues":issues,"explicit_missing_data":missing}

def graph(con,root,depth=3):
    seen=set()
    def walk(oid,d):
        if oid in seen:return {"object_id":oid,"cycle_or_repeat":True}
        r=con.execute("SELECT object_id,object_type,label,evidence_state,status FROM code_objects WHERE object_id=?",(oid,)).fetchone()
        if not r:return {"missing":oid}
        seen.add(oid)
        node=dict(r);node["children"]=[]
        if d>0:
            for e in con.execute("SELECT * FROM edges WHERE source_object_id=? ORDER BY edge_type,target_object_id",(oid,)):
                node["children"].append({"edge":dict(e),"node":walk(e["target_object_id"],d-1)})
        return node
    return walk(root,depth)

def export_all(con):
    tabs=["meta","artifacts","taxa","experiments","code_objects","occurrences","edges","measurements","annotations","claims","claim_links"]
    return {t:rows(con.execute(f"SELECT * FROM {t}")) for t in tabs}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",default=str(DEFAULT_DB))
    sp=ap.add_subparsers(dest="cmd",required=True)
    sp.add_parser("stats")
    p=sp.add_parser("list");p.add_argument("object_type",nargs="?");p.add_argument("--state")
    p=sp.add_parser("show");p.add_argument("id")
    p=sp.add_parser("graph");p.add_argument("id");p.add_argument("--depth",type=int,default=3)
    p=sp.add_parser("sequence");p.add_argument("sequence")
    p=sp.add_parser("measurements");p.add_argument("subject_id")
    p=sp.add_parser("claims");p.add_argument("--state")
    sp.add_parser("verify")
    p=sp.add_parser("export-json");p.add_argument("path")
    a=ap.parse_args()
    con=connect(a.db)
    try:
        if a.cmd=="stats":
            print(json.dumps(stats(con),indent=2))
        elif a.cmd=="list":
            q="SELECT object_id,object_type,label,evidence_state,status,data_completeness FROM code_objects WHERE 1=1";v=[]
            if a.object_type:q+=" AND object_type=?";v.append(a.object_type)
            if a.state:q+=" AND evidence_state=?";v.append(a.state)
            print(json.dumps(rows(con.execute(q+" ORDER BY object_type,object_id",v)),indent=2))
        elif a.cmd=="show":
            d=object_payload(con,a.id) or experiment_payload(con,a.id)
            if not d:raise SystemExit("Not found: "+a.id)
            print(json.dumps(d,indent=2))
        elif a.cmd=="graph":
            print(json.dumps(graph(con,a.id,a.depth),indent=2))
        elif a.cmd=="sequence":
            s=a.sequence.upper().strip()
            print(json.dumps(rows(con.execute(
                "SELECT object_id,object_type,label,sequence,length_bp FROM code_objects WHERE sequence=? OR (sequence IS NOT NULL AND instr(sequence,?)>0) ORDER BY length_bp DESC",
                (s,s))),indent=2))
        elif a.cmd=="measurements":
            print(json.dumps(rows(con.execute("SELECT * FROM measurements WHERE subject_id=? ORDER BY measurement_id",(a.subject_id,))),indent=2))
        elif a.cmd=="claims":
            cur=con.execute("SELECT * FROM claims WHERE evidence_state=? ORDER BY claim_id",(a.state,)) if a.state else con.execute("SELECT * FROM claims ORDER BY claim_id")
            print(json.dumps(rows(cur),indent=2))
        elif a.cmd=="verify":
            r=verify(con);print(json.dumps(r,indent=2));raise SystemExit(0 if r["ok"] else 2)
        elif a.cmd=="export-json":
            pathlib.Path(a.path).write_text(json.dumps(export_all(con),indent=2),encoding="utf-8")
            print("Wrote",pathlib.Path(a.path).resolve())
    finally:
        con.close()

if __name__=="__main__":
    main()
