export interface DeviceMotion {
  id: number;
  caseId?: number | null;
  patientId?: number | null;
  timestamp?: Date | null;
  movementIndex0100?: number | null;
  microMovementsCount?: number | null;
  bedExitDetected01?: number | null;
  fallEvent01?: number | null;
  impactMagnitudeG?: number | null;
  postFallImmobilityMinutes?: number | null;
}
