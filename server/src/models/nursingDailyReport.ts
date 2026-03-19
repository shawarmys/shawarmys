import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { NursingDailyReport } from "../types/nursingDailyReport.js";
import CaseModel from "./case.js";

@Entity("nursing_daily_reports")
export class NursingDailyReportModel implements NursingDailyReport {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: number | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  ward?: string | null;

  @Column({ name: "report_date", type: "date", nullable: true })
  reportDate?: Date | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  shift?: string | null;

  @Column({ name: "nursing_note_free_text", type: "text", nullable: true })
  nursingNoteFreeText?: string | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
