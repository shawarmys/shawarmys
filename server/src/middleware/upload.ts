import { Request } from "express";
import multer, { FileFilterCallback } from "multer";
import os from "os";
import path from "path";

const ALLOWED_EXTENSIONS = new Set([".csv", ".xlsx", ".pdf"]);

const upload = multer({
  storage: multer.diskStorage({
    destination: os.tmpdir(),
    filename: (req, file, next) => {
      next(null, file.originalname);
    },
  }),
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

export default upload;
