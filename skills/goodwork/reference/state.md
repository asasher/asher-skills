# state - v2 workspace state model

This is the single source of truth for Goodwork v2 state. If a matcher, scheduler, approval flow, or presentation layer consumes it, it is JSON/JSONL. If a person or the interview consumes it, it is Markdown.

## Workspace shape

One project folder is one person. The `goodwork/` folder holds state, vendored UI assets, the persistent Chrome profile, and a gitignored `.env`. Never install Goodwork globally. Degrade to draft-and-instruct when a capability is absent.

## Writer rule

The agent is the sole writer of state files. The server never mutates JSON or Markdown and never appends approvals; it only appends user request events to `events.jsonl`. The agent drains events, validates them, and writes resulting state changes.

## IDs

Every JSON record has a stable `id`, generated once and never reused. Use lowercase prefixes plus a sortable suffix: `tgt_`, `src_`, `lead_`, `pipe_`, `act_`, `art_`, `draft_`, `reply_`, `appr_`, `evt_`, `metric_`, `ev_`. Cross-file links use IDs, not names, URLs, or row numbers. Events that become approvals link by `source_event_id`; pipeline cards keep `target_id`, `lead_id`, `approval_ids`, `artifact_ids`, `drafts`, and `proof_ids`.

## Operational Files

- `pipeline.json`: live CRM cards, compacted inbound reply summaries, drafts, and next actions.
  Schema: `{version, updated_at, cards:[{id,target_id?,lead_id?,role,stage,warmth,last_touch_at?,next_action?,due_at?,owner,status,reason_code?,thread_ids:[],replies:[{id,channel,received_at,from,summary,stage_signal?,event_id?}],reply_digest?,drafts:[{id,channel,provider_draft_id?,thread_id?,artifact_id,content_hash,created_at,status}],artifact_ids:[],approval_ids:[],proof_ids:[]}], unmatched_replies:[{id,channel,received_at,from,summary,match_candidates:[],status}]}`.
- `leads.json`: posting leads found by `scout`, including the bench.
  Schema: `{version, updated_at, leads:[{id,source_id,target_id?,title,org,url,location?,posted_at?,found_at,score,status,score_reasons:[],must_haves:[],evidence_coverage?,pipeline_id?}]}`.
- `sources.json`: boards, newsletters, communities, saved searches, and job channels.
  Schema: `{version, updated_at, sources:[{id,type,name,url?,query?,niche_tags:[],cadence,status,last_swept_at?,auth_required,notes?}]}`.
- `targets.json`: employer/segment target list and Top 10.
  Schema: `{version, updated_at, targets:[{id,name,kind,segment?,location?,url?,scores:{advocacy,motivation,posting},rank?,status,reason_codes:[],insider_ids:[],notes?}]}`.
- `capabilities.json`: setup results and best available execution rungs.
  Schema: `{version, updated_at, workspace_id, connectors:{gmail,calendar}, chrome:{profile_path,status,sites:{}}, tailscale:{status,magicdns_url?}, ui:{diffs_vendor,status}, reconcile:{cadence,last_run_at?}, execution:{rungs:[]}, notifications:{status}}`.
- `metrics.json`: quotas and weekly funnel metrics.
  Schema: `{version, updated_at, quotas:{weekly_applications}, weeks:[{week_start,outreach_sent,applications,screens,interviews,offers,response_rate?,notes?}]}`.
- `evidence-inbox.json`: pending profile evidence queue.
  Schema: `{version, updated_at, entries:[{id,event_id?,source,source_id?,profile_sections:[],claim,status,created_at,drained_at?}]}`.
- `approvals.jsonl`: append-only agent-written approval records, one JSON object per line.
  Record schema: `{id,timestamp,item_id,channel,granularity,content_hash,covers:[],source_event_id?,approved_by,expires_at?}`.
- `events.jsonl`: append-only server-written request events, one JSON object per line.
  Record schema: `{id,timestamp,session_id,type,actor,page,item_id?,content_hash?,granularity?,covers:[],payload:{},tags:[]}`.

## Narrative Files

- `PROFILE.md`: the Good Work Profile, confidence marks, dated changelog.
- `ODYSSEYS.md`: alternative futures and gauges.
- `EXPERIMENTS.md`: prototypes, craft moves, small bets, debriefs.
- `NICHE.md`: positioning hypotheses, two-pager, community map, visibility plan.
- `JOURNAL.md`: Good Time Journal and weekly reviews.

Legacy `TARGETS.md` and `PIPELINE.md` may be read during migration, but v2 authority is `targets.json` and `pipeline.json`.

## Evidence Inbox

Profile-relevant events are queued in `evidence-inbox.json`: lead approvals/dismissals, CV rejection reasons, recurring reply reason codes, stage-change patterns, and prototype debriefs. `profile` and `review` drain this inbox into dated `PROFILE.md` updates using the confidence-mark discipline, then mark inbox entries drained or dismissed.
