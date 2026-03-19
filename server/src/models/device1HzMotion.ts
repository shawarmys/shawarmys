import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
} from "typeorm";
import type { Device1HzMotion } from "../types/device1HzMotion";
import CaseModel from "./case";

@Entity("device_1hz_motions")
export default class Device1HzMotionModel implements Device1HzMotion {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ name: "case_id", type: "bigint", nullable: true })
  caseId?: number | null;

  @Column({ name: "patient_id", type: "bigint", nullable: true })
  patientId?: number | null;

  @Column({ name: "device_id", type: "varchar", length: 256, nullable: true })
  deviceId?: string | null;

  @Column({ type: "timestamp", nullable: true })
  timestamp?: Date | null;

  @Column({ name: "bed_occupied_0_1", type: "int", nullable: true })
  bedOccupied01?: number | null;

  @Column({ name: "movement_score_0_100", type: "float", nullable: true })
  movementScore0100?: number | null;

  @Column({ name: "accel_x_m_s2", type: "float", nullable: true })
  accelXMs2?: number | null;

  @Column({ name: "accel_y_m_s2", type: "float", nullable: true })
  accelYMs2?: number | null;

  @Column({ name: "accel_z_m_s2", type: "float", nullable: true })
  accelZMs2?: number | null;

  @Column({ name: "accel_magnitude_g", type: "float", nullable: true })
  accelMagnitudeG?: number | null;

  @Column({ name: "pressure_zone1_0_100", type: "float", nullable: true })
  pressureZone10100?: number | null;

  @Column({ name: "pressure_zone2_0_100", type: "float", nullable: true })
  pressureZone20100?: number | null;

  @Column({ name: "pressure_zone3_0_100", type: "float", nullable: true })
  pressureZone30100?: number | null;

  @Column({ name: "pressure_zone4_0_100", type: "float", nullable: true })
  pressureZone40100?: number | null;

  @Column({ name: "bed_exit_event_0_1", type: "int", nullable: true })
  bedExitEvent01?: number | null;

  @Column({ name: "bed_return_event_0_1", type: "int", nullable: true })
  bedReturnEvent01?: number | null;

  @Column({ name: "fall_event_0_1", type: "int", nullable: true })
  fallEvent01?: number | null;

  @Column({ name: "impact_magnitude_g", type: "float", nullable: true })
  impactMagnitudeG?: number | null;

  @Column({ name: "event_id", type: "varchar", length: 256, nullable: true })
  eventId?: string | null;

  @ManyToOne(() => CaseModel)
  @JoinColumn()
  case?: CaseModel;
}
