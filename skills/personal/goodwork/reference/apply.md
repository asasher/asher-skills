# apply - high-fit applications, evidence-gated

Applications convert warmth into process; they rarely create warmth. Apply deliberately to high-fit targets, ideally with an insider referral already working.

## Execution

Read [execution.md](execution.md) before creating an application package: it owns the ladder, approvals, hashes, evidence gate, quota gate, proof capture, and the Gmail draft exception. This command decides whether to apply and prepares the truthful package.

## Decide whether to apply at all

Score the posting against the profile before any tailoring:
- **Fit**: does the actual work (tasks, not title) feed the energy map? Does the org pass the values/dealbreaker check and decent-work floor?
- **Evidence**: run the evidence gate against must-have requirements. If it fails, the fix is a proof artifact (`assets`) or a prototype, not adjectives.
- **Warmth**: is there an insider, or a plausible path to one this week? Cold-applying to a Top 5 target *wastes the target* — it files the user into the portal pile before outreach could route them. For Top 10 targets, default order: outreach first, apply second (or simultaneously *with* the referral, when the insider advises it).
- Verify the posting is real and current — stale and ghost postings are common.

If the `eloquent` skill is available, its `analyze-job` command does the parsing/scoring mechanics; feed it the profile and add the warmth/energy checks above.

## Produce the application

Delegate document mechanics to eloquent (`tailor`, `ats`, `cover-letter`) with the profile and `NICHE.md` as inputs; without eloquent, apply the same rules directly:
- Mirror the posting's real keywords only where true evidence exists; standard headings; simple formatting; no stuffing, no invented anything.
- Cover letter (when asked for): the niche story applied to why-them-specifically, three sentences of proof, one link to the most relevant artifact.
- Reuse the same verified evidence base across applications — tailoring is selection and emphasis, not rewriting reality.

## After submitting

- Log in `pipeline.json`: date, version sent, referral status, follow-up date (insider nudge ~1 week; portal-only, expect silence and let the pipeline carry it).
- Quota sanity: 5–10 high-fit applications/week beats 50 sprayed. Application-to-screen under ~10% over 15+ applications → stop and diagnose in `review`: targeting, evidence gaps, or documents — in that order.

## Output

The application package or Gmail draft, the `pipeline.json` entry with follow-up dates, and — where the evidence gate failed — the named gap and the cheapest artifact that would close it.
