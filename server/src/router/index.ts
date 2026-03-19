import { Router } from "express";
import { controller } from "../controller/index.js";
import upload from "../middleware/upload.js";

export const apiRouter = Router();

// --- Health & Root ---
apiRouter.get("/", controller.getRoot);
apiRouter.get("/health", controller.getHealth);

// --- Metadata ---
apiRouter.get("/metadata", controller.getMetadata);

// --- Imported Files ---
apiRouter.get("/imported-files", controller.getImportedFiles);

// --- Data Sources Summary ---
apiRouter.get("/data-sources-summary", controller.getDataSourcesSummary);

// --- Data Groups Summary ---
apiRouter.get("/data-groups-summary", controller.getDataGroupsSummary);

// --- File Upload ---
apiRouter.post("/upload", upload.single("file"), controller.uploadFile);

apiRouter.post("/upload/array", controller.upload2dArray);
