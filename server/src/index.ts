import "dotenv/config";
import express from "express";
import helmet from "helmet";
import { initializeDataSource } from "./db";

const app = express();
const PORT = process.env.PORT || 4000;

app.use(helmet());
app.use(express.json());

(async function bootstrap() {
  try {
    await initializeDataSource();

    // Import router after DataSource is ready so that module-level
    // getDB() calls in services resolve against an initialized connection.
    const { apiRouter } = await import("./router");
    app.use("/api", apiRouter);

    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (err) {
    console.error("Failed to start server", err);
    process.exit(1);
  }
})();
