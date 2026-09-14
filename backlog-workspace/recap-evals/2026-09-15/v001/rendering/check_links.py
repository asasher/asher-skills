from html.parser import HTMLParser
from pathlib import Path
import urllib.request,concurrent.futures,json,datetime
D=Path(__file__).parent
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=set()
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   u=dict(attrs).get('href','')
   if u.startswith('https://'):self.links.add(u)
p=Links();p.feed((D.parent/'report.html').read_text())
def check(u):
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,method='HEAD',headers={'User-Agent':'Asher-Skills-Recap-Check'}),timeout=25)
  return {'url':u,'status':r.status,'final_url':r.url}
 except Exception as e:return {'url':u,'error':str(e)}
r=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(check,sorted(p.links)))
(D/'external-link-checks.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'links':r},indent=2))
print('External links checked:',len(r));print('Failures:',[x for x in r if x.get('status')!=200])
