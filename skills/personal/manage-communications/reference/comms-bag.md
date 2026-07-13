# Comms bag

A comms bag is the immutable handoff between evidence selection and rendering. Create one per audience.

## Shape

```json
{
  "schema_version": 1,
  "id": "2026-07-13-pipelines-al-arkan-001",
  "kind": "project_update",
  "generated_at": "2026-07-13T09:00:00+04:00",
  "subject": "Pipelines — project update",
  "preheader": "Verified progress and next steps",
  "audience_id": "pipelines-al-arkan",
  "project_ids": ["pipelines"],
  "summary": "Short evidence-backed summary.",
  "sections": [
    {
      "title": "Shipped",
      "items": [
        {
          "status": "shipped",
          "title": "RFQ workflow",
          "detail": "Visible client-safe detail.",
          "evidence_ids": ["git:abc123"]
        }
      ]
    }
  ],
  "evidence": [
    {
      "id": "git:abc123",
      "source": "/absolute/or-stable-source-reference",
      "observed_at": "2026-07-12T16:20:00+04:00",
      "status": "production_verified",
      "feature": "rfq-management"
    }
  ]
}
```

`kind` is `project_update` or `internal_digest`. An internal digest uses either the lens layout — `Delivery`,
`Pending`, `Cash`, and `Growth` — or one delivery section per project/client followed by `Cash` and `Growth`.
In the project/client layout, pending delivery work stays inside its project and is identified by item status.
Empty lens sections remain visible as “Nothing verified for this period.”

Every visible item cites at least one evidence ID. The visible copy never exposes hashes, internal file
paths, private notes, or evidence IDs. Those remain in the bag and run manifest.

The bag is complete when its schema validates, every evidence ID resolves exactly once, each item is allowed
for the selected audience, and its audience/evidence hashes can be computed deterministically.
