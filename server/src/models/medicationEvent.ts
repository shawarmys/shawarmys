import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { MedicationEvent } from "../types/medicationEvent.js";
import CaseModel from "./case.js";

@Entity("medication_events")
export class MedicationEventModel implements MedicationEvent {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "record_type", type: "varchar", length: 256, nullable: true })
  recordType?: string | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: number | null;

  @Column({
    name: "encounter_id",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  encounterId?: string | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  ward?: string | null;

  @Column({ name: "admission_datetime", type: "timestamp", nullable: true })
  admissionDatetime?: Date | null;

  @Column({ name: "discharge_datetime", type: "timestamp", nullable: true })
  dischargeDatetime?: Date | null;

  @Column({ name: "order_id", type: "varchar", length: 256, nullable: true })
  orderId?: string | null;

  @Column({ name: "order_uuid", type: "varchar", length: 256, nullable: true })
  orderUuid?: string | null;

  @Column({
    name: "medication_code_atc",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  medicationCodeAtc?: string | null;

  @Column({
    name: "medication_name",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  medicationName?: string | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  route?: string | null;

  @Column({ type: "float", nullable: true })
  dose?: number | null;

  @Column({ name: "dose_unit", type: "varchar", length: 256, nullable: true })
  doseUnit?: string | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  frequency?: string | null;

  @Column({ name: "order_start_datetime", type: "timestamp", nullable: true })
  orderStartDatetime?: Date | null;

  @Column({ name: "order_stop_datetime", type: "timestamp", nullable: true })
  orderStopDatetime?: Date | null;

  @Column({ name: "is_prn_0_1", type: "int", nullable: true })
  isPrn01?: number | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  indication?: string | null;

  @Column({
    name: "prescriber_role",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  prescriberRole?: string | null;

  @Column({
    name: "order_status",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  orderStatus?: string | null;

  @Column({
    name: "administration_datetime",
    type: "timestamp",
    nullable: true,
  })
  administrationDatetime?: Date | null;

  @Column({ name: "administered_dose", type: "float", nullable: true })
  administeredDose?: number | null;

  @Column({
    name: "administered_unit",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  administeredUnit?: string | null;

  @Column({
    name: "administration_status",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  administrationStatus?: string | null;

  @Column({ type: "varchar", length: 256, nullable: true })
  note?: string | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
