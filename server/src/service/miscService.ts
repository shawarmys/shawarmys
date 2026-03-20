import fs from "fs";
import child_process from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";
const MISC_DR = path.join(__dirname, "..", "misc");
const PYTHON_VENV_PATH = path.join(MISC_DR, "venv", "bin", "python");
const PYTHON_CLEAN_DATA = path.join(MISC_DR, "data_cleaner", "data_cleaner.py");
const PYTHON_NORMALIZE_HEADERS = path.join(
  MISC_DR,
  "data_cleaner",
  "data_cleaner.py",
);

const execFile = promisify(child_process.execFile);

class MiscService {
  async normalizeHeaderFromFile(file: Express.Multer.File) {
    const stdout = await this.callNormalizationScript(file.path);

    const csvPath = stdout.trim().split(";")[0];
    const errorPath = stdout.trim().split(";")[1];

    const csvFileContent = fs.readFileSync(csvPath, "utf-8");
    const errorFileContent = fs.readFileSync(errorPath, "utf-8");

    const csvData = this.convertCsvTo2dArray(csvFileContent);
    const errorData = JSON.parse(errorFileContent);

    return {
      csvData,
      errorData,
    };
  }

  async normallizeHeaderFromRequest(filename: string) {
    const stdout = await this.callNormalizationScript(filename);

    const csvPath = stdout.trim().split(";")[0];
    const errorPath = stdout.trim().split(";")[1];

    const csvFileContent = fs.readFileSync(csvPath, "utf-8");
    const errorFileContent = fs.readFileSync(errorPath, "utf-8");

    const csvData = this.convertCsvTo2dArray(csvFileContent);
    const errorData = JSON.parse(errorFileContent);

    return {
      csvData,
      errorData,
    };
  }

  private async callNormalizationScript(filepath: string) {
    let out: string;
    try {
      const { stdout, stderr } = await execFile(PYTHON_VENV_PATH, [
        PYTHON_CLEAN_DATA,
        "--file_path",
        filepath,
      ]);

      out = stdout;
      console.log(stderr);
    } catch (error) {
      console.error("Error processing file:", error);
      throw new Error("Failed to process the uploaded file");
    }
    if (out) return out;
    throw new Error("Stdout empty");
  }

  async cleanData(filePath: string, ignoreOutliers?: boolean) {
    const stdout = await this.callCleaningScript(filePath, ignoreOutliers);

    const jsonPath = stdout.trim().split(";")[0];
    const csvPath = stdout.trim().split(";")[1];
    const jsonFileContent = fs.readFileSync(jsonPath, "utf-8");
    const csvFileContent = fs.readFileSync(csvPath, "utf-8");

    const jsonData = JSON.parse(jsonFileContent);
    const csvData = this.convertCsvTo2dArray(csvFileContent);

    if (ignoreOutliers) {
      const dataPath = stdout.trim().split(";")[2];
      const dataFileContent = fs.readFileSync(dataPath, "utf-8");
      const data = JSON.parse(dataFileContent);

      return {
        jsonData,
        csvData,
        data,
      };
    }

    return {
      jsonData,
      csvData,
    };
  }

  async callCleaningScript(filePath: string, ignoreOutliers?: boolean) {
    let out: string;
    const args = [PYTHON_NORMALIZE_HEADERS, "--file-path", filePath];
    ignoreOutliers && args.push("--json");
    try {
      const { stdout, stderr } = await execFile(PYTHON_VENV_PATH, args);
      out = stdout;
      console.log("stdout:", stdout);
      console.error("stderr:", stderr);
    } catch (error) {
      console.error("Error processing file:", error);
      throw new Error("Failed to process the uploaded file");
    }
    if (out) return out;
    throw new Error("cleaning data returned nothing");
  }

  convert2dArrayToCsv(arr: string[][]): string {
    return arr.map((row) => row.join(",")).join("\n");
  }

  private convertCsvTo2dArray(csv: string): string[][] {
    return csv
      .trim()
      .split("\n")
      .map((row) => row.split(","));
  }

  cleanupFiles(filePaths: string[]) {
    for (const filePath of filePaths) {
      try {
        fs.unlinkSync(filePath);
      } catch (error) {
        console.warn(`Failed to delete temp file: ${filePath}`, error);
      }
    }
  }
}

export const miscService = new MiscService();
