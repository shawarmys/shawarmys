import "dotenv/config";
import express from "express";
import helmet from "helmet";
import { initializeDataSource } from "./db";
import { apiRouter } from "./router";

const app = express();
const PORT = process.env.PORT || 4000;

app.use(helmet());
app.use(express.json());

app.use("/api", apiRouter);

(async function bootstrap() {
  try {
    await initializeDataSource();
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (err) {
    console.error("Failed to start server", err);
    process.exit(1);
  }
})();
