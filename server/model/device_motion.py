import datetime
from typing import Optional

from database import Base
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class DeviceMotions(Base):
    __tablename__ = "device_motions"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", ForeignKey("patients.id"))
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column("timestamp", DateTime)
    movement_index_0_100: Mapped[Optional[str]] = mapped_column("movement_index_0_100", String(256))
    micro_movements_count: Mapped[Optional[str]] = mapped_column("micro_movements_count", String(256))
    bed_exit_detected_0_1: Mapped[Optional[str]] = mapped_column("bed_exit_detected_0_1", String(256))
    fall_event_0_1: Mapped[Optional[str]] = mapped_column("fall_event_0_1", String(256))
    impact_magnitude_g: Mapped[Optional[str]] = mapped_column("impact_magnitude_g", String(256))
    post_fall_immobility_minutes: Mapped[Optional[str]] = mapped_column("post_fall_immobility_minutes", String(256))

    def __repr__(self) -> str:
        return f"<DeviceMotionData id={self.id} patient_id={self.patient_id}>"
