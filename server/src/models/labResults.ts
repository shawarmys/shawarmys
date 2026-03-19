import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";
import type { LabResults } from "../types/labResults.js";

@Entity("lab_results")
export class LabResultsModel implements LabResults {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: string | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  sex?: string | null;

  @Column({ name: "age_years", type: "int", nullable: true })
  ageYears?: number | null;

  @Column({ name: "specimen_datetime", type: "timestamp", nullable: true })
  specimenDatetime?: Date | null;

  // Sodium
  @Column({ name: "sodium_mmol_L", type: "float", nullable: true })
  sodiumMmolL?: number | null;

  @Column({ name: "sodium_flag", type: "varchar", length: 256, nullable: true })
  sodiumFlag?: string | null;

  @Column({ name: "sodium_ref_low", type: "float", nullable: true })
  sodiumRefLow?: number | null;

  @Column({ name: "sodium_ref_high", type: "float", nullable: true })
  sodiumRefHigh?: number | null;

  // Potassium
  @Column({ name: "potassium_mmol_L", type: "float", nullable: true })
  potassiumMmolL?: number | null;

  @Column({
    name: "potassium_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  potassiumFlag?: string | null;

  @Column({ name: "potassium_ref_low", type: "float", nullable: true })
  potassiumRefLow?: number | null;

  @Column({ name: "potassium_ref_high", type: "float", nullable: true })
  potassiumRefHigh?: number | null;

  // Creatinine
  @Column({ name: "creatinine_mg_dL", type: "float", nullable: true })
  creatinineMgDl?: number | null;

  @Column({
    name: "creatinine_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  creatinineFlag?: string | null;

  @Column({ name: "creatinine_ref_low", type: "float", nullable: true })
  creatinineRefLow?: number | null;

  @Column({ name: "creatinine_ref_high", type: "float", nullable: true })
  creatinineRefHigh?: number | null;

  // eGFR
  @Column({ name: "egfr_mL_min_1_73m2", type: "float", nullable: true })
  egfrMlMin173m2?: number | null;

  @Column({ name: "egfr_flag", type: "varchar", length: 256, nullable: true })
  egfrFlag?: string | null;

  @Column({ name: "egfr_ref_low", type: "float", nullable: true })
  egfrRefLow?: number | null;

  @Column({ name: "egfr_ref_high", type: "float", nullable: true })
  egfrRefHigh?: number | null;

  // Glucose
  @Column({ name: "glucose_mg_dL", type: "float", nullable: true })
  glucoseMgDl?: number | null;

  @Column({
    name: "glucose_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  glucoseFlag?: string | null;

  @Column({ name: "glucose_ref_low", type: "float", nullable: true })
  glucoseRefLow?: number | null;

  @Column({ name: "glucose_ref_high", type: "float", nullable: true })
  glucoseRefHigh?: number | null;

  // Hemoglobin
  @Column({ name: "hemoglobin_g_dL", type: "float", nullable: true })
  hemoglobinGDl?: number | null;

  @Column({ name: "hb_flag", type: "varchar", length: 256, nullable: true })
  hbFlag?: string | null;

  @Column({ name: "hb_ref_low", type: "float", nullable: true })
  hbRefLow?: number | null;

  @Column({ name: "hb_ref_high", type: "float", nullable: true })
  hbRefHigh?: number | null;

  // WBC
  @Column({ name: "wbc_10e9_L", type: "float", nullable: true })
  wbc10e9L?: number | null;

  @Column({ name: "wbc_flag", type: "varchar", length: 256, nullable: true })
  wbcFlag?: string | null;

  @Column({ name: "wbc_ref_low", type: "float", nullable: true })
  wbcRefLow?: number | null;

  @Column({ name: "wbc_ref_high", type: "float", nullable: true })
  wbcRefHigh?: number | null;

  // Platelets
  @Column({ name: "platelets_10e9_L", type: "float", nullable: true })
  platelets10e9L?: number | null;

  @Column({
    name: "platelets_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  plateletsFlag?: string | null;

  @Column({ name: "plt_ref_low", type: "float", nullable: true })
  pltRefLow?: number | null;

  @Column({ name: "plt_ref_high", type: "float", nullable: true })
  pltRefHigh?: number | null;

  // CRP
  @Column({ name: "crp_mg_L", type: "float", nullable: true })
  crpMgL?: number | null;

  @Column({ name: "crp_flag", type: "varchar", length: 256, nullable: true })
  crpFlag?: string | null;

  @Column({ name: "crp_ref_low", type: "float", nullable: true })
  crpRefLow?: number | null;

  @Column({ name: "crp_ref_high", type: "float", nullable: true })
  crpRefHigh?: number | null;

  // ALT
  @Column({ name: "alt_U_L", type: "float", nullable: true })
  altUL?: number | null;

  @Column({ name: "alt_flag", type: "varchar", length: 256, nullable: true })
  altFlag?: string | null;

  @Column({ name: "alt_ref_low", type: "float", nullable: true })
  altRefLow?: number | null;

  @Column({ name: "alt_ref_high", type: "float", nullable: true })
  altRefHigh?: number | null;

  // AST
  @Column({ name: "ast_U_L", type: "float", nullable: true })
  astUL?: number | null;

  @Column({ name: "ast_flag", type: "varchar", length: 256, nullable: true })
  astFlag?: string | null;

  @Column({ name: "ast_ref_low", type: "float", nullable: true })
  astRefLow?: number | null;

  @Column({ name: "ast_ref_high", type: "float", nullable: true })
  astRefHigh?: number | null;

  // Bilirubin
  @Column({ name: "bilirubin_mg_dL", type: "float", nullable: true })
  bilirubinMgDl?: number | null;

  @Column({
    name: "bilirubin_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  bilirubinFlag?: string | null;

  @Column({ name: "bili_ref_low", type: "float", nullable: true })
  biliRefLow?: number | null;

  @Column({ name: "bili_ref_high", type: "float", nullable: true })
  biliRefHigh?: number | null;

  // Albumin
  @Column({ name: "albumin_g_dL", type: "float", nullable: true })
  albuminGDl?: number | null;

  @Column({
    name: "albumin_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  albuminFlag?: string | null;

  @Column({ name: "albumin_ref_low", type: "float", nullable: true })
  albuminRefLow?: number | null;

  @Column({ name: "albumin_ref_high", type: "float", nullable: true })
  albuminRefHigh?: number | null;

  // INR
  @Column({ type: "float", nullable: true })
  inr?: number | null;

  @Column({ name: "inr_flag", type: "varchar", length: 256, nullable: true })
  inrFlag?: string | null;

  @Column({ name: "inr_ref_low", type: "float", nullable: true })
  inrRefLow?: number | null;

  @Column({ name: "inr_ref_high", type: "float", nullable: true })
  inrRefHigh?: number | null;

  // Lactate
  @Column({ name: "lactate_mmol_L", type: "float", nullable: true })
  lactateMmolL?: number | null;

  @Column({
    name: "lactate_flag",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  lactateFlag?: string | null;

  @Column({ name: "lactate_ref_low", type: "float", nullable: true })
  lactateRefLow?: number | null;

  @Column({ name: "lactate_ref_high", type: "float", nullable: true })
  lactateRefHigh?: number | null;
}
