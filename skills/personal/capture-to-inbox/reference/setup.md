# Setup

Reconcile a project-bound capture instance. Local materialization is deterministic; external installation,
deployment, Shortcut build, and the smoke test are effect gates.

## Sequence

1. **Inspect.** Locate the consumer root and existing `control-plane/` instance, config, external dependency
   lock, provider binding, API source, and Shortcut artifacts. Record local edits and incomplete prior steps.
2. **Resolve external capability.** Detect `build-apple-shortcuts`. If absent or incompatible, disclose the
   exact `metadata.external` identity: Shortcuts Playground, Federico Viticci/MacStories, MIT license,
   upstream source, Codex plugin kind, `1.2.x` policy, project/user install scope, Read/Write capability, and
   its optional post-edit validation hook. Obtain explicit consent, install through the active harness's
   Codex-plugin provider, then verify a resolved `1.2.x` manifest, the `shortcuts-playground` skill, validator,
   and signer. Record the resolution in setup-owned `external-dependencies.lock.json`, separate from
   `skills-lock.json`. Rejected consent leaves setup incomplete without installing or enabling hooks.
3. **Materialize.** Run:

   ```bash
   python3 <capture-to-inbox-skill>/scripts/setup_instance.py --project <consumer-root>
   ```

   It creates a missing Inbox, API source, config/state/deployment skeletons, an empty Shortcut working
   directory, a private project-root `.env` ignored by Git, and its `capture_to_inbox.token_file` instance
   binding. Preserve an existing token while tightening `.env` to mode `0600`. A conflict exit is a
   reconciliation gate: inspect each candidate and consumer edit; never copy over it wholesale.
4. **Deploy.** Follow [deployment](deployment.md). Bind Railway initially, create or reuse persistent storage,
   set provider-managed secrets, deploy only the consumer API copy, and effect-verify health and auth before
   recording non-secret identities.
5. **Build Shortcut.** Give [shortcut-contract](shortcut-contract.md) to the verified external skill. Generate
   XML inside the consumer instance, validate it, sign it, and verify the signed output. Never copy prototype
   XML or `build_shortcut.py` into the installed skill or consumer instance.
6. **Smoke test.** Submit one Shortcut-shaped text capture and one small file capture; list both queue items;
   run the drain once with `--dry-run` and once normally; verify the Inbox has one Queue-ID marker per item,
   the attachment bytes and checksum match, and the remote queue is empty. Remove only the smoke entries and
   files whose IDs were recorded by this run if the consumer does not want them retained.
7. **Record.** Mark setup complete only when external capability, materialization, local `.env`, deployment,
   generated and signed Shortcut, and the end-to-end smoke test all pass. Store no secret values in tracked
   files or setup state.

## Reconciliation

Reruns compare API files with `template.json`. Unedited managed files may advance to the shipped template;
consumer-modified files produce adjacent candidate files and a nonzero exit. Existing config, state,
deployment bindings, Inbox contents, XML, and signed artifacts are preserved. Recheck live effects and repair
only missing or stale steps; never create parallel Railway resources or regenerate active XML blindly.

Completion criterion: the recorded provider endpoint accepts a real authenticated capture, the generated and
signed Shortcut satisfies its contract, a verified drain writes exactly once locally before deleting
remotely, and an immediate rerun changes nothing.
