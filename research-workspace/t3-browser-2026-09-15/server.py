import http.server,json,os,time
from urllib.parse import urlparse
ROOT=os.path.dirname(__file__)
PAGE='''<!doctype html><html><head><title>T3 browser experiment</title><style>body{font:18px system-ui;max-width:680px;margin:40px auto;padding:20px}button,input{font:inherit;padding:8px;margin:8px}#result{padding:20px;background:#edf4ff}@media(prefers-color-scheme:dark){body{background:#18202c;color:white}#result{background:#31415c}}</style></head><body><h1>T3 browser experiment</h1><p id="host"></p><p id="session"></p><label>Name <input id="name" aria-label="Name"></label><button id="login">Sign in to test app</button><p id="result" role="status">Ready</p><button id="save">Save change</button><script>
const $=s=>document.querySelector(s);async function state(){const s=await(await fetch('/state')).json();$('#host').textContent='Server: '+s.host;$('#session').textContent='Test cookie: '+(s.cookie||'none');return s}state();$('#login').onclick=async()=>{await fetch('/login',{method:'POST'});localStorage.setItem('t3-probe','local-marker');sessionStorage.setItem('t3-probe','tab-marker');await state();$('#result').textContent='Signed in as '+$('#name').value};$('#save').onclick=async()=>{$('#result').textContent='Saving';const r=await fetch('/save',{method:'POST'});$('#result').textContent=r.ok?'Saved successfully':'Save failed';if(!r.ok)console.error('Probe save failed: '+r.status)};
</script></body></html>'''
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/state': self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(json.dumps({'host':os.uname().nodename,'cookie':'; '.join(c.strip() for c in self.headers.get('Cookie','').split(';') if c.strip().startswith('t3_probe_'))}).encode())
  else: self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(PAGE.encode())
 def do_POST(self):
  if self.path=='/clear':
   self.send_response(200);self.send_header('Set-Cookie','t3_probe_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0');self.send_header('Set-Cookie','t3_probe_persistent=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0')
  elif self.path=='/login':
   self.send_response(200);self.send_header('Set-Cookie','t3_probe_session=demo-session; HttpOnly; SameSite=Lax; Path=/');self.send_header('Set-Cookie','t3_probe_persistent=demo-persistent; HttpOnly; SameSite=Lax; Path=/; Max-Age=3600')
  else: time.sleep(.2);self.send_response(500 if open(ROOT+'/save-mode').read().strip()=='broken' else 200)
  self.end_headers();self.wfile.write(b'{}')
http.server.ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('PROBE_PORT','48765'))),Handler).serve_forever()
