import cors from "cors";
import express from "express";
import helmet from "helmet";
import { apiRouter } from "./router";

const app = express();
const PORT = process.env.PORT || 4000;

app.use(helmet());
app.use(
  cors({
    origin: [
      "http://localhost:3000",
      "http://127.0.0.1:3000",
      "http://localhost:80",
      "http://127.0.0.1:80",
    ],
    credentials: true,
  }),
);
app.use(express.json());

app.use("/api", apiRouter);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
