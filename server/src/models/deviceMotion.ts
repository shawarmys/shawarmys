import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { DeviceMotion } from "../types/deviceMotion.js";
import CaseModel from "./case.js";

@Entity("device_motions")
export class DeviceMotionModel implements DeviceMotion {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: number | null;

  @Column({ type: "timestamp", nullable: true })
  timestamp?: Date | null;

  @Column({ name: "movement_index_0_100", type: "float", nullable: true })
  movementIndex0100?: number | null;

  @Column({ name: "micro_movements_count", type: "int", nullable: true })
  microMovementsCount?: number | null;

  @Column({ name: "bed_exit_detected_0_1", type: "int", nullable: true })
  bedExitDetected01?: number | null;

  @Column({ name: "fall_event_0_1", type: "int", nullable: true })
  fallEvent01?: number | null;

  @Column({ name: "impact_magnitude_g", type: "float", nullable: true })
  impactMagnitudeG?: number | null;

  @Column({
    name: "post_fall_immobility_minutes",
    type: "float",
    nullable: true,
  })
  postFallImmobilityMinutes?: number | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn({ name: "case_id" })
  case?: CaseModel;
}
