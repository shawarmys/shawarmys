import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";
import type { Case } from "../types/case.js";

@Entity("cases")
export default class CaseModel implements Case {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "patient_id", type: "bigint" })
  patientId: number;

  @Column({ name: "admission_date", type: "date", nullable: true })
  admissionDate?: Date | null;

  @Column({ name: "discharge_date", type: "date", nullable: true })
  dischargeDate?: Date | null;
}
