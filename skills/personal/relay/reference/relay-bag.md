# Relay bag

The bag is the immutable handoff between selection and rendering. Create one per audience with schema version
2. It contains visible email content and private evidence attribution, but no provider credential.

```json
{
  "schema_version": 2,
  "id": "fixture-client-2026-07-16-a1b2c3d4e5f6",
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

Every bag uses the locally bound ordered section recipe. Whether an empty section is rendered, omitted, or
given fallback copy is repository-owned editorial policy implemented by the local template; the bag preserves
the bound recipe so that choice remains deterministic. Every visible item cites at least one evidence ID that
resolves exactly once. Visible HTML/text never exposes evidence IDs, source paths, selection rules, prompts, or
private notes.

Validation is complete when `scripts/validate_relay_bag.py <bag> --repository-root <repo>` passes, recipients
are normalized and disjoint, the bag still matches the structured audience and interest bindings, all evidence
references resolve, and canonical JSON hashing is deterministic.
