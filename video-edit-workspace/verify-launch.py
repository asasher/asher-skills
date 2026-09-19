from pathlib import Path
import json,re,sys
out=Path(__file__).resolve().parent / 'evals' / sys.argv[1];run=json.loads((out/'run.json').read_text());log=Path.home()/('.t3/userdata/logs/provider/events.'+run['thread_id']+'.log');meta=None
for line in log.read_text().splitlines():
 if ' NTIVE: ' not in line:continue
 try:d=json.loads(line.split(' NTIVE: ',1)[1])
 except ValueError:continue
 if d.get('method')=='thread/started':meta=d['payload']['thread'];break
assert meta,'No thread/started event'
path=Path(meta['path']);catalog=[];context=None;reads=[]
for line in path.read_text().splitlines():
 try:d=json.loads(line)
 except ValueError:continue
 p=d.get('payload',{})
 if d.get('type')=='turn_context':context={k:p.get(k) for k in ['cwd','model','effort','approval_policy','sandbox_policy']}
 if p.get('type')=='message':
  text='\n'.join(c.get('text','') for c in p.get('content',[]))
  if '### Available skills' in text:
   catalog=[l for l in text.splitlines() if l.startswith('- ') and '(file:' in l]
 if p.get('type') in ['function_call','custom_tool_call']:
  text=p.get('arguments',p.get('input',''))
  if 'SKILL.md' in text:reads.append({'call_id':p.get('call_id'),'tool':p.get('name'),'arguments':text})
names=[re.match(r'- ([^:]+):',x).group(1) for x in catalog]
expected={'diagram-design','edit-video','motion-graphics','unslop','watch-video','writing-for-humans'}
record={'t3_thread_id':run['thread_id'],'provider_thread_id':meta['id'],'provider_rollout':str(path),'actual_cwd':meta['cwd'],'context':context,'available_skill_names':names,'exact_skill_set':set(names)==expected,'observed_skill_calls':reads}
save=out/'launch-evidence.json';save.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='observed_skill_calls'},indent=2))
assert record['exact_skill_set'],names
assert meta['cwd']==run['directory']
assert context['model']==run['settings']['model'] and context['effort']==run['settings']['effort']
