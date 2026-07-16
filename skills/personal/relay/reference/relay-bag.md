# Relay bag

The bag is the immutable handoff between selection and rendering. Create one per audience with schema version
2. It contains visible email content and private evidence attribution, but no provider credential.

```json
{
  "schema_version": 2,
  "id": "fixture-project-update-001",
  "kind": "project_update",
  "generated_at": "2026-07-16T09:00:00Z",
  "subject": "Project — update",
  "preheader": "Verified progress and next steps",
  "audience_id": "fixture-client",
  "project_ids": ["fixture-project"],
  "sender": "relay@fixture.invalid",
  "recipients": {"to": ["recipient@fixture.invalid"], "cc": ["operator@fixture.invalid"]},
  "summary": "Short evidence-backed summary.",
  "sections": [{
    "title": "Shipped",
    "items": [{
      "status": "production_verified",
      "title": "Example capability",
      "detail": "The capability is available.",
      "evidence_ids": ["fixture:evidence:1"]
    }]
  }],
  "evidence": [{
    "id": "fixture:evidence:1",
    "source": "fixture",
    "observed_at": "2026-07-15T16:20:00Z",
    "status": "production_verified",
    "project_id": "fixture-project",
    "feature": "example-capability"
  }]
}
```

An internal digest uses the locally bound ordered section recipe. Empty required sections remain visible as
“Nothing verified for this period.” Every visible item cites at least one evidence ID that resolves exactly
once. Visible HTML/text never exposes evidence IDs, source paths, selection rules, prompts, or private notes.

Validation is complete when `scripts/validate_relay_bag.py` passes, recipients are normalized and disjoint,
all evidence references resolve, and canonical JSON hashing is deterministic.
