#!/usr/bin/env python3
"""Coordinate an ordinary video-production thread; keep evidence outside its project."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'video-edit-workspace/evals'


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def inspect(thread):
    database = Path.home() / '.t3/userdata/state.sqlite'
    con = sqlite3.connect('file:' + str(database) + '?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    try:
        con.execute('BEGIN')
        one = lambda sql: next((dict(r) for r in con.execute(sql, (thread,))), None)
        many = lambda sql: [dict(r) for r in con.execute(sql, (thread,))]
        return {
            'thread': one('SELECT thread_id,title,worktree_path,model_selection_json,runtime_mode,interaction_mode,deleted_at FROM projection_threads WHERE thread_id=?'),
            'session': one('SELECT status,provider_name,provider_instance_id,provider_thread_id,active_turn_id,last_error FROM projection_thread_sessions WHERE thread_id=?'),
            'turns': many('SELECT turn_id,state,started_at,completed_at FROM projection_turns WHERE thread_id=? ORDER BY requested_at,row_id'),
            'messages': many('SELECT message_id,turn_id,role,text,is_streaming,created_at,updated_at,attachments_json FROM projection_thread_messages WHERE thread_id=? ORDER BY created_at,rowid'),
        }
    finally:
        con.rollback()
        con.close()


def verify(run):
    project = Path(run['directory'])
    for relative, expected in run['package_hashes'].items():
        if sha(project / relative) != expected:
            raise RuntimeError('Participant package changed: ' + relative)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['prepare','start','status','capture'])
    p.add_argument('iteration')
    p.add_argument('--directory', type=Path)
    p.add_argument('--prompt-file', type=Path)
    p.add_argument('--thread-helper', type=Path)
    p.add_argument('--provider', default='codex')
    a = p.parse_args()
    if not a.iteration.startswith('iteration-') or not a.iteration[10:].isdigit():
        p.error('Use iteration-N')
    out = BASE / a.iteration
    if a.command == 'prepare':
        if not all([a.directory,a.prompt_file,a.thread_helper]):
            p.error('prepare needs directory, prompt-file, and thread-helper')
        project = a.directory.resolve()
        prompt = a.prompt_file.read_text()
        # Test identities and rubric stay in this coordinator directory.
        if any(x in prompt.lower() for x in ['eval','benchmark','under test']):
            raise RuntimeError('Use an ordinary production prompt')
        out.mkdir(parents=True, exist_ok=False)
        (out/'prompt.txt').write_text(prompt)
        initial = out/'project-inputs'
        initial.mkdir()
        for name in ['AGENTS.md','DESIGN.md','TOOLS.md','.codex/config.toml','package.json','bun.lock']:
            src=project/name
            if src.exists():
                dest=initial/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
        package_hashes = {str(f.relative_to(project)):sha(f) for f in sorted((project/'.agents/skills').rglob('*')) if f.is_file()}
        run = {'created_at':now(),'name':'OBS September 19 · Educational edit','status':'prepared','directory':str(project),'branch':'main',
               'source_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
               'project_initial_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=project,text=True).strip(),
               'settings':{'provider':a.provider,'model':'gpt-6-astra','effort':'high','service_tier':'default','runtime_mode':'full-access','harness':'T3 Code'},
               'thread_helper':str(a.thread_helper.resolve()),'thread_helper_sha256':sha(a.thread_helper),'prompt_sha256':sha(out/'prompt.txt'),
               'package_hashes':package_hashes,'inputs':[{'name':f.name,'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted((project/'raw').iterdir()) if f.is_file()],
               'thread_id':None,'format':'landscape','format_basis':'Coordinator stated a landscape working assumption after optional format question; no human format selection received before preparation.',
               'human_review':'pending','isolation':'Standalone project; task-only prompt; six copied production skills; workspace-scoped disabling of ambient skills/plugins. Full-access remains enabled; this is context isolation, not a filesystem sandbox.'}
        save(out/'run.json',run)
        print(json.dumps({'status':run['status'],'directory':str(project),'inputs':[i['name'] for i in run['inputs']]}))
        return
    run=json.loads((out/'run.json').read_text())
    if a.command == 'start':
        if run['status']!='prepared' or run['thread_id']:
            raise RuntimeError('Launch already attempted. Inspect status before any retry.')
        verify(run)
        if sha(out/'prompt.txt')!=run['prompt_sha256'] or sha(Path(run['thread_helper']))!=run['thread_helper_sha256']:
            raise RuntimeError('Launch inputs changed')
        s=run['settings']
        command=[sys.executable,run['thread_helper'],'--name',run['name'],'--prompt',(out/'prompt.txt').read_text(),'--project-directory','/Users/asher/Projects/asher-skills','--directory',run['directory'],'--branch',run['branch'],'--provider',s['provider'],'--effort-option-id','reasoningEffort','--model',s['model'],'--effort',s['effort'],'--service-tier',s['service_tier'],'--runtime-mode',s['runtime_mode']]
        run['status']='launch_attempted';save(out/'run.json',run)
        result=subprocess.run(command,capture_output=True,text=True)
        (out/'dispatch.stdout').write_text(result.stdout);(out/'dispatch.stderr').write_text(result.stderr)
        try:
            dispatch=json.loads(result.stdout);run['thread_id']=dispatch.get('thread_id');save(out/'dispatch.json',dispatch)
        except ValueError:
            dispatch={}
        run['dispatch_exit_code']=result.returncode
        run['status']='start_acknowledged' if result.returncode==0 else 'launch_uncertain'
        save(out/'run.json',run)
        print(json.dumps({'status':run['status'],'thread_id':run['thread_id'],'detail':dispatch}))
        if result.returncode:raise SystemExit(result.returncode)
        return
    if not run['thread_id']:raise RuntimeError('No recorded thread identity')
    evidence=inspect(run['thread_id'])
    if a.command=='status':
        print(json.dumps({'thread':evidence['thread'],'session':evidence['session'],'turns':evidence['turns'],'recent_messages':evidence['messages'][-3:]},indent=2))
        return
    if (evidence['session'] or {}).get('active_turn_id') or any(m['is_streaming'] for m in evidence['messages']):
        raise RuntimeError('Participant still running; capture only after the turn settles')
    capture=out/('capture-'+str(len(list(out.glob('capture-*')))+1));capture.mkdir()
    save(capture/'thread.json',evidence)
    (capture/'transcript.md').write_text('\n\n'.join('## '+m['role']+' · '+m['message_id']+'\n\n'+m['text'] for m in evidence['messages']))
    project=Path(run['directory'])
    artifacts=[]
    for sub in ['output','work']:
        for f in sorted((project/sub).rglob('*')):
            if f.is_file():artifacts.append({'path':str(f.relative_to(project)),'bytes':f.stat().st_size,'sha256':sha(f)})
    save(capture/'artifacts.json',artifacts)
    verify(run)
    run['status']='captured';run['last_capture']=str(capture.relative_to(ROOT));run['human_review']='pending';save(out/'run.json',run)
    print(json.dumps({'capture':str(capture),'artifacts':len(artifacts),'human_review':'pending'}))


if __name__ == '__main__':main()
