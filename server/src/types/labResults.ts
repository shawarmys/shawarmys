export interface LabResults {
  id: number;
  caseId?: number | null;
  patientId?: string | null;
  sex?: string | null;
  ageYears?: number | null;
  specimenDatetime?: Date | null;

  sodiumMmolL?: number | null;
  sodiumFlag?: string | null;
  sodiumRefLow?: number | null;
  sodiumRefHigh?: number | null;

  potassiumMmolL?: number | null;
  potassiumFlag?: string | null;
  potassiumRefLow?: number | null;
  potassiumRefHigh?: number | null;

  creatinineMgDl?: number | null;
  creatinineFlag?: string | null;
  creatinineRefLow?: number | null;
  creatinineRefHigh?: number | null;

  egfrMlMin173m2?: number | null;
  egfrFlag?: string | null;
  egfrRefLow?: number | null;
  egfrRefHigh?: number | null;

  glucoseMgDl?: number | null;
  glucoseFlag?: string | null;
  glucoseRefLow?: number | null;
  glucoseRefHigh?: number | null;

  hemoglobinGDl?: number | null;
  hbFlag?: string | null;
  hbRefLow?: number | null;
  hbRefHigh?: number | null;

  wbc10e9L?: number | null;
  wbcFlag?: string | null;
  wbcRefLow?: number | null;
  wbcRefHigh?: number | null;

  platelets10e9L?: number | null;
  plateletsFlag?: string | null;
  pltRefLow?: number | null;
  pltRefHigh?: number | null;

  crpMgL?: number | null;
  crpFlag?: string | null;
  crpRefLow?: number | null;
  crpRefHigh?: number | null;

  altUL?: number | null;
  altFlag?: string | null;
  altRefLow?: number | null;
  altRefHigh?: number | null;

  astUL?: number | null;
  astFlag?: string | null;
  astRefLow?: number | null;
  astRefHigh?: number | null;

  bilirubinMgDl?: number | null;
  bilirubinFlag?: string | null;
  biliRefLow?: number | null;
  biliRefHigh?: number | null;

  albuminGDl?: number | null;
  albuminFlag?: string | null;
  albuminRefLow?: number | null;
  albuminRefHigh?: number | null;

  inr?: number | null;
  inrFlag?: string | null;
  inrRefLow?: number | null;
  inrRefHigh?: number | null;

  lactateMmolL?: number | null;
  lactateFlag?: string | null;
  lactateRefLow?: number | null;
  lactateRefHigh?: number | null;
}
