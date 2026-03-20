import fs from "fs";
import os from "os";
import path from "path";
import { dbService } from "./dbService";
import { miscService } from "./miscService";

class Service {
  getRoot() {
    return { message: "Server is running" };
  }

  getHealth() {
    return { status: "ok" };
  }

  async handleFileUpload(file: Express.Multer.File) {
    const { csvData, errorData } =
      await miscService.normalizeHeaderFromFile(file);

    const message = errorData["errors"];

    if (!message)
      throw new Error("Unexpected error format from normalization script");

    if (message === "valid") {
      const {
        jsonData,
        csvData: cleanedCsv,
        data,
      } = await miscService.cleanData(file.path);
      if (data) {
        await dbService.saveData(data, file.originalname);
      }
      return { jsonData, csvData: cleanedCsv };
    }

    return { csvData, errorData };
  }

  async handleArrayUpload(
    arr: string[][],
    filename: string,
    ignoreOutliers?: boolean,
  ) {
    const csv = miscService.convert2dArrayToCsv(arr);
    const tmpPath = path.join(os.tmpdir(), filename);
    await fs.promises.writeFile(tmpPath, csv, "utf8");
    const { csvData, errorData } =
      await miscService.normallizeHeaderFromRequest(tmpPath);
    const message = errorData["errors"];

    if (!message)
      throw new Error("Unexpected error format from normalization script");

    if (message === "valid") {
      const {
        jsonData,
        csvData: cleanedCsv,
        data,
      } = await miscService.cleanData(tmpPath, ignoreOutliers);
      if (data) {
        await dbService.saveData(data, filename);
      }
      return { jsonData, csvData: cleanedCsv };
    }

    return { csvData, errorData };
  }

  async getMetadata() {
    // TODO: wire up DB query
    return { importedFiles: 0, successfulMappings: 0, mappingAlerts: 0 };
  }

  async getImportedFiles() {
    // TODO: wire up DB query
    return [];
  }

  async getDataSourcesSummary() {
    // TODO: wire up DB query
    return [];
  }

  async getDataGroupsSummary() {
    // TODO: wire up DB query
    return [];
  }
}

export const service = new Service();
