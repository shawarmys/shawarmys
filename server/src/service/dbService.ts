import { getDB } from "../db/index.js";
import Device1HzMotionModel from "../models/device1HzMotion.js";
import { DeviceMotionModel } from "../models/deviceMotion.js";
import { Icd10DataModel } from "../models/icd10Data.js";
import { ImportAcDataModel } from "../models/importAcData.js";
import { IntegrationMappingModel } from "../models/integrationMapping.js";
import { LabResultsModel } from "../models/labResults.js";
import { MedicationEventModel } from "../models/medicationEvent.js";
import { NursingDailyReportModel } from "../models/nursingDailyReport.js";

const FILE_KEYWORDS = [
  "device_raw",
  "device",
  "icd",
  "labs",
  "medication",
  "nursing",
];

class DbService {
  private device1HzMotionRepository =
    getDB().getRepository(Device1HzMotionModel);
  private deviceMotionRepository = getDB().getRepository(DeviceMotionModel);
  private icd10DataRepository = getDB().getRepository(Icd10DataModel);
  private importAcDataRepository = getDB().getRepository(ImportAcDataModel);
  private integrationMappingRepository = getDB().getRepository(
    IntegrationMappingModel,
  );
  private labResultsRepository = getDB().getRepository(LabResultsModel);
  private medicationEventRepository =
    getDB().getRepository(MedicationEventModel);
  private nursingDailyReportRepository = getDB().getRepository(
    NursingDailyReportModel,
  );

  async saveData(data: any, filename: string) {
    const matchingRepository = this.matchFileName(filename);
    const insertResult = await matchingRepository.insert(data);
    if (
      !insertResult ||
      !insertResult.identifiers ||
      insertResult.identifiers.length === 0
    ) {
    }
  }

  private matchFileName(fileName: string) {
    const name = fileName.toLowerCase();

    if (name.includes("device_raw_1hz") || name.includes("device_1hz")) {
      return this.device1HzMotionRepository;
    }

    for (const keyword of FILE_KEYWORDS) {
      if (!name.includes(keyword)) continue;
      switch (keyword) {
        case "device_raw":
          return this.device1HzMotionRepository;
        case "device":
          return this.deviceMotionRepository;
        case "icd":
          return this.icd10DataRepository;
        case "labs":
          return this.labResultsRepository;
        case "medication":
          return this.medicationEventRepository;
        case "nursing":
          return this.nursingDailyReportRepository;
        default:
          break;
      }
    }

    throw new Error(`Could not match file name to repository: ${fileName}`);
  }
}

export const dbService = new DbService();
