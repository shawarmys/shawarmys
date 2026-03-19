import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { Icd10Data } from "../types/icd10Data.js";
import CaseModel from "./case.js";

@Entity("icd10_data")
export class Icd10DataModel implements Icd10Data {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: number | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  ward?: string | null;

  @Column({ name: "admission_date", type: "date", nullable: true })
  admissionDate?: Date | null;

  @Column({ name: "discharge_date", type: "date", nullable: true })
  dischargeDate?: Date | null;

  @Column({ name: "length_of_stay_days", type: "int", nullable: true })
  lengthOfStayDays?: number | null;

  @Column({
    name: "primary_icd10_code",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  primaryIcd10Code?: string | null;

  @Column({
    name: "primary_icd10_description_en",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  primaryIcd10DescriptionEn?: string | null;

  @Column({
    name: "secondary_icd10_codes",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  secondaryIcd10Codes?: string | null;

  @Column({
    name: "secondary_icd10_descriptions_en",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  secondaryIcd10DescriptionsEn?: string | null;

  @Column({ name: "ops_codes", type: "varchar", length: 256, nullable: true })
  opsCodes?: string | null;

  @Column({
    name: "ops_descriptions_en",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  opsDescriptionsEn?: string | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
