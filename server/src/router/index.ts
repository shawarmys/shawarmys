import { Request, Router } from "express";
import multer, { FileFilterCallback } from "multer";
import path from "path";
import { controller } from "../controller/index.js";

export const apiRouter = Router();

const ALLOWED_EXTENSIONS = new Set([".csv", ".xlsx", ".pdf"]);

const upload = multer({
  storage: multer.diskStorage({ destination: "/tmp" }),
  fileFilter: (
    _req: Request,
    file: Express.Multer.File,
    cb: FileFilterCallback,
  ) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (ALLOWED_EXTENSIONS.has(ext)) {
      cb(null, true);
    } else {
      cb(
        new Error(
          `File type not allowed. Accepted: ${[...ALLOWED_EXTENSIONS].join(", ")}`,
        ),
      );
    }
  },
});

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
apiRouter.get("/api/data-groups-summary", controller.getDataGroupsSummary);

// --- File Upload ---
apiRouter.post("/api/upload", upload.single("file"), controller.uploadFile);
