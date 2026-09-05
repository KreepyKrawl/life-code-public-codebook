#!/usr/bin/env python3
"""LIFE-CODE Codebook v0.8 local database server. Standard library only."""
import json,sqlite3,pathlib,urllib.parse
from http.server import BaseHTTPRequestHandler,HTTPServer

HERE=pathlib.Path(__file__).resolve().parent
DB=HERE/"LIFE_CODE_CODEBOOK_CONTINUATION_v0.8.sqlite"
UI=HERE/"LIFE_CODE_CODEBOOK_UI_v0.8.html"

def con():
    x=sqlite3.connect(DB);x.row_factory=sqlite3.Row;return x
def rows(cur):return [dict(r) for r in cur.fetchall()]
def obj(c,oid):
    o=c.execute("SELECT * FROM code_objects WHERE object_id=?",(oid,)).fetchone()
    if not o:return None
    art=c.execute("SELECT * FROM artifacts WHERE artifact_id=?",(o["source_artifact_id"],)).fetchone()
    return {"object":dict(o),
      "edges_out":rows(c.execute("SELECT * FROM edges WHERE source_object_id=? ORDER BY edge_type,target_object_id",(oid,))),
      "edges_in":rows(c.execute("SELECT * FROM edges WHERE target_object_id=? ORDER BY edge_type,source_object_id",(oid,))),
      "annotations":rows(c.execute("SELECT * FROM annotations WHERE subject_type='OBJECT' AND subject_id=? ORDER BY annotation_type",(oid,))),
      "artifact":dict(art) if art else None}
class H(BaseHTTPRequestHandler):
    def sendj(self,x,status=200):
        b=json.dumps(x,indent=2).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        p=urllib.parse.urlparse(self.path)
        if p.path=="/":
            b=UI.read_bytes();self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b);return
        c=con()
        try:
            if p.path=="/api/objects":
                q=urllib.parse.parse_qs(p.query).get("q",[""])[0]
                if q:
                    x=f"%{q}%";cur=c.execute("SELECT object_id,object_type,label,evidence_state,status FROM code_objects WHERE object_id LIKE ? OR label LIKE ? OR description LIKE ? ORDER BY object_type,object_id",(x,x,x))
                else:cur=c.execute("SELECT object_id,object_type,label,evidence_state,status FROM code_objects ORDER BY object_type,object_id")
                self.sendj(rows(cur));return
            if p.path.startswith("/api/object/"):
                oid=urllib.parse.unquote(p.path.split("/",3)[3]);d=obj(c,oid);self.sendj(d or {"error":"not found"},200 if d else 404);return
            self.sendj({"error":"not found"},404)
        finally:c.close()
    def log_message(self,fmt,*args):print("[LIFE-CODE]",fmt%args)
if __name__=="__main__":
    print("LIFE-CODE Codebook v0.8: http://127.0.0.1:8765/")
    print("CTRL+C to stop. No cloud required.")
    HTTPServer(("127.0.0.1",8765),H).serve_forever()
