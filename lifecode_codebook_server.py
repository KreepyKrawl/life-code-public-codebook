#!/usr/bin/env python3
"""Local read-only Core v0.10 site and API; standard library only."""
import json,pathlib,urllib.parse
from http.server import SimpleHTTPRequestHandler,HTTPServer
from lifecode_codebook import connect,object_payload,DEFAULT_DB,rows
HERE=pathlib.Path(__file__).resolve().parent
class H(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(HERE),**kwargs)
 def do_GET(self):
  p=urllib.parse.urlparse(self.path)
  if not p.path.startswith('/api/'):return super().do_GET()
  c=connect(DEFAULT_DB)
  try:
   status=200
   if p.path=='/api/objects':
    q=urllib.parse.parse_qs(p.query).get('q',[''])[0];x='%'+q+'%'
    data=rows(c.execute('SELECT object_id,object_type,label,evidence_state,status FROM code_objects WHERE object_id LIKE ? OR label LIKE ? OR description LIKE ? ORDER BY object_type,object_id',(x,x,x)))
   elif p.path.startswith('/api/object/'):
    data=object_payload(c,urllib.parse.unquote(p.path.split('/',3)[3]));status=200 if data else 404
   else:data={'error':'not found'};status=404
   b=json.dumps(data,indent=2).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
  finally:c.close()
if __name__=='__main__':
 print('LIFE-CODE Core v0.10: http://127.0.0.1:8765/')
 HTTPServer(('127.0.0.1',8765),H).serve_forever()
