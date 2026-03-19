export interface Device1HzMotion {
  id: number;
  caseId?: number | null;
  patientId?: number | null;
  deviceId?: string | null;
  timestamp?: Date | null;
  bedOccupied01?: number | null;
  movementScore0100?: number | null;
  accelXMs2?: number | null;
  accelYMs2?: number | null;
  accelZMs2?: number | null;
  accelMagnitudeG?: number | null;
  pressureZone10100?: number | null;
  pressureZone20100?: number | null;
  pressureZone30100?: number | null;
  pressureZone40100?: number | null;
  bedExitEvent01?: number | null;
  bedReturnEvent01?: number | null;
  fallEvent01?: number | null;
  impactMagnitudeG?: number | null;
  eventId?: string | null;
}
