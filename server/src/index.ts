import express from "express";
import helmet from "helmet";
import { apiRouter } from "./router";

const app = express();
const PORT = process.env.PORT || 4000;

app.use(helmet());
app.use(express.json());

app.use("/api", apiRouter);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
