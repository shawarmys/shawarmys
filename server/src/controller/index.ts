import { NextFunction, Request, Response } from "express";
import { service } from "../service/index.js";

class Controller {
  getRoot(req: Request, res: Response, next: NextFunction) {
    try {
      res.status(200).json(service.getRoot());
    } catch (error) {
      next(error);
    }
  }

  getHealth(req: Request, res: Response, next: NextFunction) {
    try {
      res.status(200).json(service.getHealth());
    } catch (error) {
      res.status(500).json({ error: "Internal server error" });
    }
  }

  async getMetadata(req: Request, res: Response, next: NextFunction) {
    try {
      const data = await service.getMetadata();
      res.json(data);
    } catch (error) {
      next(error);
    }
  }

  async getImportedFiles(req: Request, res: Response, next: NextFunction) {
    try {
      const data = await service.getImportedFiles();
      res.json(data);
    } catch (error) {
      next(error);
    }
  }

  async getDataSourcesSummary(req: Request, res: Response, next: NextFunction) {
    try {
      const data = await service.getDataSourcesSummary();
      res.json(data);
    } catch (error) {
      next(error);
    }
  }

  async getDataGroupsSummary(req: Request, res: Response, next: NextFunction) {
    try {
      const data = await service.getDataGroupsSummary();
      res.json(data);
    } catch (error) {
      next(error);
    }
  }

  async uploadFile(req: Request, res: Response, next: NextFunction) {
    try {
      if (!req.file) {
        res.status(400).json({ error: "No file provided" });
        return;
      }
      const result = await service.handleFileUpload(req.file);
      res.json(result);
    } catch (error) {
      next(error);
    }
  }
  async upload2dArray(req: Request, res: Response, next: NextFunction) {
    try {
      const { filename, tableData, ignoreOutliers } = req.body;
      const result = await service.handleArrayUpload(
        tableData,
        filename,
        ignoreOutliers,
      );
      res.json(result);
    } catch (error) {
      next(error);
    }
  }
}

export const controller = new Controller();
