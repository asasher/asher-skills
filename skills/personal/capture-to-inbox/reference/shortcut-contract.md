# Queue to Inbox Shortcut Contract

This is the input contract for the external `shortcuts-playground` capability. Generate the Shortcut XML in
the consumer instance; no XML template ships with this skill.

## Behavior

The Shortcut is named **Queue to Inbox**, accepts share-sheet text, URLs, images, audio, video, PDFs, and
files, and may also run without share-sheet input to ask for text. For each input item it:

1. collects optional context once per run;
2. sends one authenticated `POST <api_url>/capture` as `multipart/form-data`;
3. includes `source=ios-shortcut`, a user-approved non-secret client label, an ISO-8601 `captured_at`,
   `context`, `item_index`, and available `shared_item`, `shared_input_text`, and `shared_urls` fields;
4. sends binary input in the `payload` form field without converting media to text;
5. treats only a `201` response containing `ok: true` and an item `id` as success, and reports failed items
   without claiming the run completed.

The API URL and bearer token are Shortcut import questions or otherwise user-supplied configuration. They
must not be embedded in source XML committed to the consumer project.

## Build Gate

Invoke `shortcuts-playground` by name to author the smallest complete plist XML at
`control-plane/capture-to-inbox/shortcut/Queue to Inbox.xml`. Follow its required reading and icon resolver,
validate to a clean result, sign it, and verify the signed `.shortcut` exists and is non-empty. Record the
resolved plugin version, validation result, signing mode, source XML checksum, and generated output path in
`shortcut/build.json`; keep the signed artifact out of version control unless the consumer explicitly chooses
otherwise.

On rerun, generate changed XML to a candidate file, show the semantic action diff, and replace the active XML
only with approval. A valid but unsigned XML is not complete.
