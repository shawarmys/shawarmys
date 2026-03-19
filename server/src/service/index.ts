import fs from "fs";
import child_process from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";

const execFile = promisify(child_process.execFile);

const MISC_DR = path.join(__dirname, "..", "misc");
const PYTHON_VENV_PATH = path.join(MISC_DR, "venv", "bin", "python");
const PYTHON_SCRIPT_PATH = path.join(
  MISC_DR,
  "data_cleaner",
  "data_cleaner.py",
);

class Service {
  getRoot() {
    return { message: "Server is running" };
  }

  getHealth() {
    return { status: "ok" };
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

  async handleFileUpload(file: Express.Multer.File) {
    let jsonPath: string;
    let csvPath: string;

    try {
      const { stdout, stderr } = await execFile(PYTHON_VENV_PATH, [
        PYTHON_SCRIPT_PATH,
        "--file_path",
        file.path,
      ]);
      console.log("stdout:", stdout);
      console.error("stderr:", stderr);

      jsonPath = stdout.trim().split(";")[0];
      csvPath = stdout.trim().split(";")[1];
    } catch (error) {
      console.error("Error processing file:", error);
      throw new Error("Failed to process the uploaded file");
    }

    const jsonFile = fs.readFileSync(jsonPath, "utf-8");
    const csvFile = fs.readFileSync(csvPath, "utf-8");

    const jsonData = JSON.parse(jsonFile);
    const csvData = this.convertCsvTo2dArray(csvFile);

    return {
      jsonData,
      csvData,
    };
  }

  private convertCsvTo2dArray(csv: string): string[][] {
    return csv
      .trim()
      .split("\n")
      .map((row) => row.split(","));
  }
}

export const service = new Service();
