import datetime
from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


class DeviceMotions(Base):
    __tablename__ = "device_motions"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", ForeignKey("cases.id"))
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", BigInteger)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column("timestamp", DateTime)
    movement_index_0_100: Mapped[Optional[float]] = mapped_column("movement_index_0_100", Float)
    micro_movements_count: Mapped[Optional[int]] = mapped_column("micro_movements_count", Integer)
    bed_exit_detected_0_1: Mapped[Optional[int]] = mapped_column("bed_exit_detected_0_1", Integer)
    fall_event_0_1: Mapped[Optional[int]] = mapped_column("fall_event_0_1", Integer)
    impact_magnitude_g: Mapped[Optional[float]] = mapped_column("impact_magnitude_g", Float)
    post_fall_immobility_minutes: Mapped[Optional[float]] = mapped_column("post_fall_immobility_minutes", Float)

    def __repr__(self) -> str:
        return f"<DeviceMotionData id={self.id} patient_id={self.patient_id}>"
