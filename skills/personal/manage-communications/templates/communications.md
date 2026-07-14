# Communications Binding

This workspace is a consumer of `manage-communications`. The installed skill owns the workflow and
contracts; `control-plane/communications/` owns local policy, audiences, interests, templates, and state.

## Evidence precedence

1. Production observation or confirmation by the authoritative owner.
2. Project repository release/deployment evidence.
3. Project note event or task state.
4. Related mailbox communication.

Never upgrade a lower-confidence signal into a shipped, paid, committed, or stage-change claim.

## Audiences and interests

- A consumer may use one Markdown profile as the human-facing known home for preferences specific to a
  project–customer relationship. Link it from both entity records.
- Audience and interest files are operational manifests. When they name a profile, both must bind the same
  current SHA-256 or the run stops.
- Audience files name People dossiers; People dossiers own addresses and organization membership.
- Interest files are explicit allow/exclude maps. Unknown interest requires review, not assumption.
- External updates contain only client-relevant, externally safe evidence.
- The internal digest may be richer but keeps uncertainty, ownership, and source boundaries visible.
- The workspace may bind consumer-owned layout and editorial playbooks here. Keep brand, client, project,
  and recipient choices outside the installed skill.

## Delivery policy

- Present every rendered message, its proposed recipients, and forced light/dark previews in a browser;
  approval applies to the exact rendered-content and recipient hashes.
- AgentMail may deliver rich HTML only to the configured reviewer.
- Outlook creates forward drafts with the current audience recipients in `To`; do not add the reviewer or
  sender unless the audience includes them. No stakeholder send is automatic.
- The forward wrapper is intentional AI provenance.
- New evidence supersedes an awaiting-review draft; never silently patch it.
- Only unique Sent Items reconciliation or explicit human confirmation advances a watermark. Reconciliation
  records the actual sent recipients without rewriting the reviewed manifest.

## Local choices

Record the approved digest cadence, external coalescing rule, payment-verification owner, and any temporary
interest defaults in `control-plane/communications/policy.json`. Do not duplicate those values here.
