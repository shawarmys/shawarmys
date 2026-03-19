export interface AlertMessage {
  id: number;
  timestamp: Date;
  message: string;
  type: string;
  caseId?: number | null;
  icd10Id?: number | null;
  labResultId?: number | null;
  nursingReportId?: number | null;
  deviceMotionId?: number | null;
  device1hzMotionId?: number | null;
  medicationEventId?: number | null;
}
