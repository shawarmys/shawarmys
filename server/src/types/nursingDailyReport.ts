export interface NursingDailyReport {
  id: number;
  caseId?: number | null;
  patientId?: number | null;
  ward?: string | null;
  reportDate?: Date | null;
  shift?: string | null;
  nursingNoteFreeText?: string | null;
}
