import subprocess, pathlib, json, datetime, concurrent.futures
D=pathlib.Path('backlog-workspace/recap-evals/2026-09-15/v001/sources'); D.mkdir(parents=True,exist_ok=True)
queries={
'repository':'repos/asasher/asher-skills',
'main-branch':'repos/asasher/asher-skills/branches/main',
'releases':'repos/asasher/asher-skills/releases?per_page=100',
'deployments':'repos/asasher/asher-skills/deployments?per_page=100',
'events':'repos/asasher/asher-skills/events?per_page=100',
'merged-pr-search':'search/issues?q=repo:asasher/asher-skills+is:pr+is:merged+merged:2026-09-07..2026-09-15&per_page=100',
'pull-201':'repos/asasher/asher-skills/pulls/201',
'pull-201-commits':'repos/asasher/asher-skills/pulls/201/commits?per_page=100',
'pull-201-comments':'repos/asasher/asher-skills/issues/201/comments?per_page=100',
'pull-201-reviews':'repos/asasher/asher-skills/pulls/201/reviews?per_page=100',
'pull-201-review-comments':'repos/asasher/asher-skills/pulls/201/comments?per_page=100',
'pull-201-files':'repos/asasher/asher-skills/pulls/201/files?per_page=100',
}
def get(it):
 name,url=it; r=subprocess.run(['gh','api','--paginate','--slurp',url],text=True,capture_output=True)
 (D/(name+'.json' if r.returncode==0 else name+'.error.txt')).write_text(r.stdout if r.returncode==0 else r.stderr)
 return {'name':name,'endpoint':url,'exit_code':r.returncode,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(r.stdout),'error':r.stderr if r.returncode else None}
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(get,queries.items()))
(D/'requests.json').write_text(json.dumps(results,indent=2))
for file in ['AGENTS.md','CONTEXT.md','README.md','CHANGELOG.md','package.json','skills/software-development/backlog/SKILL.md','skills/software-development/backlog/reference/recap.md']:
 r=subprocess.run(['git','show','10f388ac6b97fbd11360a88ce94e1d460dcfc304:'+file],text=True,capture_output=True)
 (D/('revision-'+file.replace('/','__'))).write_text(r.stdout)
for name,args in {
'git-state':['rev-parse','HEAD'],
'git-week-log':['log','--format=fuller','--first-parent','--since=2026-09-07T20:02:04Z','--until=2026-09-14T20:02:04Z','10f388ac6b97fbd11360a88ce94e1d460dcfc304'],
'git-week-patches':['log','-p','--first-parent','--since=2026-09-07T20:02:04Z','--until=2026-09-14T20:02:04Z','10f388ac6b97fbd11360a88ce94e1d460dcfc304','--','skills','README.md','CHANGELOG.md','CONTEXT.md','package.json','tools/review-server.ts'],
'git-week-stat':['log','--stat','--first-parent','--since=2026-09-07T20:02:04Z','--until=2026-09-14T20:02:04Z','10f388ac6b97fbd11360a88ce94e1d460dcfc304'],
}.items():
 r=subprocess.run(['git',*args],text=True,capture_output=True); (D/(name+'.txt')).write_text(r.stdout)
print(json.dumps(results,indent=2))
