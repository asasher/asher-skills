import { createRunwayServer } from "./app.js";

const port = Number(process.env.PORT || 3000);
const server = createRunwayServer();
server.listen(port, "0.0.0.0", () => console.log(`until-zero runway API listening on ${port}`));
