#!/usr/bin/env python3
import json,sys,hashlib
from pathlib import Path
p=Path(sys.argv[1]);s=json.loads(p.read_text(encoding="utf-8"))
problems=[]
if not s.get("public_release_gates",{}).get("passed"):problems.append("release gate not passed")
for o in s.get("code_objects",[]):
    if o.get("evidence_tier")=="C":problems.append("Tier-C object: "+o["object_id"])
for a in s.get("artifacts",[]):
    if "EXP-0002" in (a.get("name","")+" "+a.get("role","")).upper():problems.append("possible EXP-0002 artifact: "+a["artifact_id"])
for o in s.get("code_objects",[]):
    if o.get("sequence") and hashlib.sha256(o["sequence"].encode()).hexdigest()!=o.get("sequence_sha256"):
        problems.append("sequence hash mismatch: "+o["object_id"])
print(json.dumps({"ok":not problems,"problems":problems,"snapshot":s.get("snapshot_schema"),"objects":len(s.get("code_objects",[]))},indent=2))
raise SystemExit(0 if not problems else 2)
