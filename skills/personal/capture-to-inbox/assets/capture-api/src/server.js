import { createCaptureServer } from "./app.js";

const port = Number(process.env.PORT || 3000);
const server = createCaptureServer();

server.listen(port, () => {
  console.log(`Capture to Inbox API listening on ${port}`);
});
