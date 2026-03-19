import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { IntegrationMapping } from "../types/integrationMapping.js";
import CaseModel from "./case.js";

@Entity("integration_mappings")
export class IntegrationMappingModel implements IntegrationMapping {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "lab_results_id", type: "bigint", nullable: true })
  labResultsId?: number | null;

  @Column({ name: "icd10_data_id", type: "bigint", nullable: true })
  icd10DataId?: number | null;

  @Column({ name: "nursing_daily_reports_id", type: "bigint", nullable: true })
  nursingDailyReportsId?: number | null;

  @Column({ name: "medication_events_id", type: "bigint", nullable: true })
  medicationEventsId?: number | null;

  @Column({ name: "device_motions_id", type: "bigint", nullable: true })
  deviceMotionsId?: number | null;

  @Column({ name: "device_1hz_motions_id", type: "bigint", nullable: true })
  device1hzMotionsId?: number | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
