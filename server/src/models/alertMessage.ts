import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { AlertMessage } from "../types/alertMessage.js";
import CaseModel from "./case.js";

@Entity("alert_messages")
export default class AlertMessageModel implements AlertMessage {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id: number;

  @Column({ type: "timestamp" })
  timestamp!: Date;

  @Column({ name: "mesage", type: "varchar", length: 256 })
  message!: string;

  @Column({ type: "varchar", length: 256 })
  type!: string;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "icd10_id", type: "bigint", nullable: true })
  icd10Id?: number | null;

  @Column({ name: "lab_result_id", type: "bigint", nullable: true })
  labResultId?: number | null;

  @Column({ name: "nursing_report_id", type: "bigint", nullable: true })
  nursingReportId?: number | null;

  @Column({ name: "device_motion_id", type: "bigint", nullable: true })
  deviceMotionId?: number | null;

  @Column({ name: "device_1hz_motion_id", type: "bigint", nullable: true })
  device1hzMotionId?: number | null;

  @Column({ name: "medication_event_id", type: "bigint", nullable: true })
  medicationEventId?: number | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
