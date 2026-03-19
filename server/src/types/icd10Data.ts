export interface Icd10Data {
  id: number;
  caseId?: number | null;
  patientId?: number | null;
  ward?: string | null;
  admissionDate?: Date | null;
  dischargeDate?: Date | null;
  lengthOfStayDays?: number | null;
  primaryIcd10Code?: string | null;
  primaryIcd10DescriptionEn?: string | null;
  secondaryIcd10Codes?: string | null;
  secondaryIcd10DescriptionsEn?: string | null;
  opsCodes?: string | null;
  opsDescriptionsEn?: string | null;
}
