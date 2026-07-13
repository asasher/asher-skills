# Capture to Inbox API

A dependency-free Node 20 HTTP API for durable, bearer-authenticated capture queues.

## Endpoints

- `GET /healthz` - public liveness and authentication-configuration status.
- `POST /capture` - authenticated `multipart/form-data`, form-encoded, or JSON capture.
- `GET /queue/items` - authenticated oldest-first queue listing.
- `GET /queue/items/:id` - authenticated metadata read.
- `GET /queue/items/:id/payload` - authenticated payload download.
- `DELETE /queue/items/:id` - authenticated drained marker.

## Environment

- `CAPTURE_TOKEN` - required bearer token.
- `QUEUE_DIR` - persistent queue path; defaults to `/data/queue`.
- `MAX_UPLOAD_MB` - total request-body limit; defaults to `100`.
- `PORT` - listen port; defaults to `3000`.

Each accepted item is written into a private temporary directory and atomically renamed into the queue. The
metadata records payload size and SHA-256 so consumers can verify bytes before deleting the remote item.

Run `npm test` without installing dependencies.
