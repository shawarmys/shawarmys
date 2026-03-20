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
    const { tableData, errors } =
      await miscService.normalizeHeaderFromFile(file);

    if (!errors)
      throw new Error("Unexpected error format from normalization script");

    if (errors === "valid") {
      const { errors, tableData, data } = await miscService.cleanData(
        file.path,
      );
      if (data) {
        await dbService.saveData(data, file.originalname);
      }
      const { outliers, nonOutlierErrors } =
        this.removeErrorsFromOutliers(errors);
      return { errors: nonOutlierErrors, tableData, outliers };
    }

    return { tableData, errors };
  }

  async handleArrayUpload(
    arr: string[][],
    filename: string,
    ignoreOutliers?: boolean,
  ) {
    const csv = miscService.convert2dArrayToCsv(arr);
    const tmpPath = path.join(os.tmpdir(), filename);
    await fs.promises.writeFile(tmpPath, csv, "utf8");
    const { tableData, errors } =
      await miscService.normallizeHeaderFromRequest(tmpPath);

    if (!errors)
      throw new Error("Unexpected error format from normalization script");

    if (errors === "valid") {
      const { errors, tableData, data } = await miscService.cleanData(
        tmpPath,
        ignoreOutliers,
      );
      if (data) {
        await dbService.saveData(data, filename);
        return;
      }
      const { outliers, nonOutlierErrors } =
        this.removeErrorsFromOutliers(errors);
      return { errors: nonOutlierErrors, tableData, outliers };
    }

    return { tableData, errors };
  }

  removeErrorsFromOutliers(errors: any) {
    const outliers = errors.filter((err: any) => err.error === "outlier");
    const nonOutlierErrors = errors.filter(
      (err: any) => err.error !== "outlier",
    );
    return { outliers, nonOutlierErrors };
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
    return ["Clinic 1", "Clinic 2", "Clinic 3", "Clinic 4"];
  }

  async getDataGroupsSummary() {
    // TODO: wire up DB query
    return ["Lab Results", "Medication Events", "Nursing Reports", "Devices"];
  }
}

export const service = new Service();
