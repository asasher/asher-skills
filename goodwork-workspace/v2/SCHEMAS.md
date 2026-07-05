# Goodwork v2 Schemas

Schemas here mirror the skill state model and add example records for implementation planning. All timestamps are ISO 8601 with timezone. IDs are stable and never reused.

## `pipeline.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "cards": [
    {
      "id": "pipe_*",
      "target_id": "tgt_* | null",
      "lead_id": "lead_* | null",
      "role": "string",
      "stage": "researching|outreach|conversation|referral|applied|screen|interview|offer|closed_won|closed_lost|retired",
      "warmth": "cold|weak_tie|insider|referral_committed",
      "last_touch_at": "datetime | null",
      "next_action": "string | null",
      "due_at": "date | null",
      "owner": "agent|user|contact",
      "status": "open|blocked|closed",
      "reason_code": "string | null",
      "thread_ids": ["string"],
      "replies": [
        {
          "id": "reply_*",
          "channel": "gmail|linkedin|whatsapp|manual",
          "received_at": "datetime",
          "from": "string",
          "summary": "string",
          "stage_signal": "string | null",
          "event_id": "evt_* | null"
        }
      ],
      "reply_digest": {
        "last_compacted_at": "datetime | null",
        "count": "number",
        "summary": "string | null",
        "source_thread_ids": ["string"]
      },
      "drafts": [
        {
          "id": "draft_*",
          "channel": "gmail|manual",
          "provider_draft_id": "string | null",
          "thread_id": "string | null",
          "artifact_id": "art_*",
          "content_hash": "sha256:*",
          "created_at": "datetime",
          "status": "created|sent|discarded"
        }
      ],
      "artifact_ids": ["art_*"],
      "approval_ids": ["appr_*"],
      "proof_ids": ["proof_*"]
    }
  ],
  "unmatched_replies": [
    {
      "id": "reply_*",
      "channel": "gmail|linkedin|whatsapp|manual",
      "received_at": "datetime",
      "from": "string",
      "summary": "string",
      "match_candidates": ["pipe_*"],
      "status": "pending|matched|dismissed"
    }
  ]
}
```

Example record:

```json
{
  "id": "pipe_20260706_01H7VJ",
  "target_id": "tgt_20260706_meridian",
  "lead_id": "lead_20260706_pm01",
  "role": "Senior Platform PM",
  "stage": "referral",
  "warmth": "insider",
  "last_touch_at": "2026-07-05T16:20:00+04:00",
  "next_action": "Wait for user to send Gmail draft to Maya",
  "due_at": "2026-07-08",
  "owner": "agent",
  "status": "open",
  "reason_code": null,
  "thread_ids": ["gmail_thr_18f82a"],
  "replies": [
    {
      "id": "reply_20260706_01",
      "channel": "gmail",
      "received_at": "2026-07-06T08:55:00+04:00",
      "from": "maya@meridian.example",
      "summary": "Maya offered to refer after seeing the tailored one-pager.",
      "stage_signal": "referral_offered",
      "event_id": null
    }
  ],
  "reply_digest": {
    "last_compacted_at": null,
    "count": 0,
    "summary": null,
    "source_thread_ids": []
  },
  "drafts": [
    {
      "id": "draft_20260706_01",
      "channel": "gmail",
      "provider_draft_id": "gmail_draft_18f82b",
      "thread_id": "gmail_thr_18f82a",
      "artifact_id": "art_outreach_20260706_01",
      "content_hash": "sha256:4f7f0c0a9b5a8fb3",
      "created_at": "2026-07-06T09:20:00+04:00",
      "status": "created"
    }
  ],
  "artifact_ids": ["art_outreach_20260706_01"],
  "approval_ids": [],
  "proof_ids": []
}
```

## `leads.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "leads": [
    {
      "id": "lead_*",
      "source_id": "src_*",
      "target_id": "tgt_* | null",
      "title": "string",
      "org": "string",
      "url": "url",
      "location": "string | null",
      "posted_at": "date | null",
      "found_at": "datetime",
      "score": "number",
      "status": "bench|queued|dismissed|promoted|applied|stale",
      "score_reasons": ["string"],
      "must_haves": ["string"],
      "evidence_coverage": "number | null",
      "pipeline_id": "pipe_* | null"
    }
  ]
}
```

Example record:

```json
{
  "id": "lead_20260706_ashby01",
  "source_id": "src_20260701_climatejobs",
  "target_id": "tgt_20260702_northstar",
  "title": "Staff Data Product Manager",
  "org": "Northstar Grid",
  "url": "https://jobs.ashbyhq.com/northstar/staff-data-pm",
  "location": "Remote US",
  "posted_at": "2026-07-02",
  "found_at": "2026-07-06T08:40:00+04:00",
  "score": 86,
  "status": "bench",
  "score_reasons": ["Top 10 target", "energy fit: systems + user feedback", "insider path exists"],
  "must_haves": ["platform PM", "data products", "enterprise customers"],
  "evidence_coverage": 0.78,
  "pipeline_id": null
}
```

## `sources.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "sources": [
    {
      "id": "src_*",
      "type": "board|newsletter|community|saved_search|recruiter|company",
      "name": "string",
      "url": "url | null",
      "query": "string | null",
      "niche_tags": ["string"],
      "cadence": "manual|daily|weekly|monthly",
      "status": "active|paused|retired",
      "last_swept_at": "datetime | null",
      "auth_required": "boolean",
      "notes": "string | null"
    }
  ]
}
```

Example record:

```json
{
  "id": "src_20260701_climatejobs",
  "type": "board",
  "name": "Climatebase product searches",
  "url": "https://climatebase.org/jobs",
  "query": "product manager data platform remote",
  "niche_tags": ["climate", "data-products", "platform"],
  "cadence": "weekly",
  "status": "active",
  "last_swept_at": "2026-07-06T08:40:00+04:00",
  "auth_required": false,
  "notes": "Produces strong leads, low duplicate rate."
}
```

## `targets.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "targets": [
    {
      "id": "tgt_*",
      "name": "string",
      "kind": "employer|project|fellowship|agency|oss|client_segment",
      "segment": "string | null",
      "location": "string | null",
      "url": "url | null",
      "scores": {
        "advocacy": "1-3",
        "motivation": "1-5",
        "posting": "1-3"
      },
      "rank": "number | null",
      "status": "top10|bench|retired|vetoed",
      "reason_codes": ["string"],
      "insider_ids": ["contact_*"],
      "notes": "string | null"
    }
  ]
}
```

Example record:

```json
{
  "id": "tgt_20260702_northstar",
  "name": "Northstar Grid",
  "kind": "employer",
  "segment": "climate infrastructure software",
  "location": "Remote US",
  "url": "https://northstar.example",
  "scores": {
    "advocacy": 2,
    "motivation": 5,
    "posting": 3
  },
  "rank": 3,
  "status": "top10",
  "reason_codes": [],
  "insider_ids": ["contact_maya_p"],
  "notes": "Strong mission fit; verify on-call expectations."
}
```

## `capabilities.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "workspace_id": "string",
  "connectors": {
    "gmail": "connected|unavailable|declined",
    "calendar": "connected|unavailable|declined"
  },
  "chrome": {
    "profile_path": "path",
    "status": "ready|missing|declined",
    "sites": {
      "linkedin": "ready|missing|declined",
      "job_boards": "ready|partial|missing",
      "whatsapp": "ready|declined|not_configured"
    }
  },
  "tailscale": {
    "status": "ready|desk_only|missing|declined",
    "magicdns_url": "url | null"
  },
  "ui": {
    "diffs_vendor": "ready|missing",
    "status": "ready|missing"
  },
  "reconcile": {
    "cadence": "manual|on-demand|scheduled",
    "last_run_at": "datetime | null"
  },
  "execution": {
    "rungs": ["mcp|ats_direct|chrome|manual"]
  },
  "notifications": {
    "status": "ready|missing|declined"
  }
}
```

Example record:

```json
{
  "version": 1,
  "updated_at": "2026-07-06T09:00:00+04:00",
  "workspace_id": "gw_asher_20260706",
  "connectors": {
    "gmail": "connected",
    "calendar": "connected"
  },
  "chrome": {
    "profile_path": "goodwork/chrome-profile",
    "status": "ready",
    "sites": {
      "linkedin": "ready",
      "job_boards": "partial",
      "whatsapp": "declined"
    }
  },
  "tailscale": {
    "status": "ready",
    "magicdns_url": "https://goodwork-asher.tailnet.example"
  },
  "ui": {
    "diffs_vendor": "ready",
    "status": "ready"
  },
  "reconcile": {
    "cadence": "on-demand",
    "last_run_at": null
  },
  "execution": {
    "rungs": ["mcp", "ats_direct", "chrome", "manual"]
  },
  "notifications": {
    "status": "ready"
  }
}
```

## `metrics.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "quotas": {
    "weekly_applications": "number"
  },
  "weeks": [
    {
      "week_start": "date",
      "outreach_sent": "number",
      "applications": "number",
      "screens": "number",
      "interviews": "number",
      "offers": "number",
      "response_rate": "number | null",
      "notes": "string | null"
    }
  ]
}
```

Example record:

```json
{
  "week_start": "2026-07-06",
  "outreach_sent": 12,
  "applications": 4,
  "screens": 1,
  "interviews": 0,
  "offers": 0,
  "response_rate": 0.18,
  "notes": "Warm intros outperformed cold messages."
}
```

## `evidence-inbox.json`

Schema:

```json
{
  "version": "number",
  "updated_at": "datetime",
  "entries": [
    {
      "id": "ev_*",
      "event_id": "evt_* | null",
      "source": "lead|pipeline|approval|reply|journal|prototype|review",
      "source_id": "string | null",
      "profile_sections": ["string"],
      "claim": "string",
      "status": "pending|drained|dismissed",
      "created_at": "datetime",
      "drained_at": "datetime | null"
    }
  ]
}
```

Example record:

```json
{
  "id": "ev_20260706_dismiss01",
  "event_id": "evt_20260706_019",
  "source": "lead",
  "source_id": "lead_20260706_ashby01",
  "profile_sections": ["Energy map", "Values"],
  "claim": "User dismissed three high-pay enterprise sales leads due to travel and quota-pressure concerns.",
  "status": "pending",
  "created_at": "2026-07-06T10:12:00+04:00",
  "drained_at": null
}
```

## `approvals.jsonl`

Record schema:

```json
{
  "id": "appr_*",
  "timestamp": "datetime",
  "item_id": "art_*|lead_*|pipe_*",
  "channel": "gmail|linkedin|ats|browser|manual|calendar",
  "granularity": "item|session_batch",
  "content_hash": "sha256:*",
  "covers": [
    {
      "item_id": "string",
      "content_hash": "sha256:*"
    }
  ],
  "source_event_id": "evt_* | null",
  "approved_by": "user",
  "expires_at": "datetime | null"
}
```

Example record:

```json
{
  "id": "appr_20260706_01",
  "timestamp": "2026-07-06T09:18:05+04:00",
  "item_id": "art_apply_20260706_02",
  "channel": "ats",
  "granularity": "item",
  "content_hash": "sha256:4f7f0c0a9b5a8fb3",
  "covers": [
    {
      "item_id": "art_apply_20260706_02",
      "content_hash": "sha256:4f7f0c0a9b5a8fb3"
    }
  ],
  "source_event_id": "evt_20260706_01H7VJ8M",
  "approved_by": "user",
  "expires_at": "2026-07-07T09:18:05+04:00"
}
```

## `events.jsonl`

Record schema:

```json
{
  "id": "evt_*",
  "timestamp": "datetime",
  "session_id": "sess_*",
  "type": "approval_requested|rejection_requested|edit_then_approve_requested|batch_approval_requested|stage_change_requested|test_tap|comment",
  "actor": "user",
  "page": "approval|diff|kanban|health",
  "item_id": "string | null",
  "content_hash": "sha256:* | null",
  "granularity": "item|session_batch|null",
  "covers": [
    {
      "item_id": "string",
      "content_hash": "sha256:*"
    }
  ],
  "payload": "object",
  "tags": ["string"]
}
```

Example record:

```json
{
  "id": "evt_20260706_01H7VJ8M",
  "timestamp": "2026-07-06T09:15:22+04:00",
  "session_id": "sess_20260706_9b2c",
  "type": "batch_approval_requested",
  "actor": "user",
  "page": "approval",
  "item_id": null,
  "content_hash": null,
  "granularity": "session_batch",
  "covers": [
    {
      "item_id": "art_outreach_20260706_01",
      "content_hash": "sha256:4f7f0c0a9b5a8fb3"
    },
    {
      "item_id": "art_apply_20260706_02",
      "content_hash": "sha256:91be8c7f5401"
    }
  ],
  "payload": {
    "action": "approve_batch"
  },
  "tags": ["approval"]
}
```

## Markdown Narrative Files

No JSON schema: `PROFILE.md`, `ODYSSEYS.md`, `EXPERIMENTS.md`, `NICHE.md`, and `JOURNAL.md`.

Legacy migration inputs only: `TARGETS.md` and `PIPELINE.md`.
