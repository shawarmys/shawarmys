export interface Case {
  id: number;
  patientId: number;
  admissionDate?: Date | null;
  dischargeDate?: Date | null;
}
