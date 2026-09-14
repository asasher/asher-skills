import subprocess,json,pathlib,concurrent.futures,datetime
D=pathlib.Path('backlog-workspace/recap-evals/2026-09-15/v001/sources')
deploys=[x for p in json.loads((D/'deployments.json').read_text()) for x in p]
queries={'issue-208':'repos/asasher/asher-skills/issues/208','issue-208-comments':'repos/asasher/asher-skills/issues/208/comments?per_page=100','pages-config':'repos/asasher/asher-skills/pages'}
for x in deploys:
 if x['created_at']>='2026-09-07T20:02:04Z': queries['deployment-'+str(x['id'])+'-statuses']=x['statuses_url']+'?per_page=100'
def get(it):
 n,u=it; r=subprocess.run(['gh','api','--paginate','--slurp',u],capture_output=True,text=True)
 (D/(n+'.json' if not r.returncode else n+'.error.txt')).write_text(r.stdout if not r.returncode else r.stderr)
 return {'name':n,'endpoint':u,'exit_code':r.returncode,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':r.stderr if r.returncode else None}
res=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(get,queries.items()));(D/'requests-more.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
