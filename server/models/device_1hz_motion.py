import datetime
from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Device1HzMotions(Base):
    __tablename__ = "device_1hz_motions"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", ForeignKey("cases.id"))
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", BigInteger)
    device_id: Mapped[Optional[str]] = mapped_column("device_id", String(256))
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column("timestamp", DateTime)
    bed_occupied_0_1: Mapped[Optional[int]] = mapped_column("bed_occupied_0_1", Integer)
    movement_score_0_100: Mapped[Optional[float]] = mapped_column("movement_score_0_100", Float)
    accel_x_m_s2: Mapped[Optional[float]] = mapped_column("accel_x_m_s2", Float)
    accel_y_m_s2: Mapped[Optional[float]] = mapped_column("accel_y_m_s2", Float)
    accel_z_m_s2: Mapped[Optional[float]] = mapped_column("accel_z_m_s2", Float)
    accel_magnitude_g: Mapped[Optional[float]] = mapped_column("accel_magnitude_g", Float)
    pressure_zone1_0_100: Mapped[Optional[float]] = mapped_column("pressure_zone1_0_100", Float)
    pressure_zone2_0_100: Mapped[Optional[float]] = mapped_column("pressure_zone2_0_100", Float)
    pressure_zone3_0_100: Mapped[Optional[float]] = mapped_column("pressure_zone3_0_100", Float)
    pressure_zone4_0_100: Mapped[Optional[float]] = mapped_column("pressure_zone4_0_100", Float)
    bed_exit_event_0_1: Mapped[Optional[int]] = mapped_column("bed_exit_event_0_1", Integer)
    bed_return_event_0_1: Mapped[Optional[int]] = mapped_column("bed_return_event_0_1", Integer)
    fall_event_0_1: Mapped[Optional[int]] = mapped_column("fall_event_0_1", Integer)
    impact_magnitude_g: Mapped[Optional[float]] = mapped_column("impact_magnitude_g", Float)
    event_id: Mapped[Optional[str]] = mapped_column("event_id", String(256))

    def __repr__(self) -> str:
        return f"<Device1HzMotionData id={self.id} patient_id={self.patient_id}>"
