from datetime import date
from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class AlertMessages(Base):
    __tablename__ = "alert_messages"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = mapped_column("timestamp", DateTime)
    message: Mapped[str] = mapped_column("mesage", String(256))
    type: Mapped[str] = mapped_column("type", String(256))
    case_id: Mapped[Optional[int]] = mapped_column("case_id", BigInteger, ForeignKey("cases.id"))\

    icd10_id: Mapped[Optional[int]] = mapped_column("icd10_id", BigInteger, ForeignKey("icd10_data.id"))
    lab_result_id: Mapped[Optional[int]] = mapped_column("lab_result_id", BigInteger, ForeignKey("lab_results.id"))
    nursing_report_id: Mapped[Optional[int]] = mapped_column("nursing_report_id", BigInteger, ForeignKey("nursing_daily_reports.id"))

    device_motion_id: Mapped[Optional[int]] = mapped_column("device_motion_id", BigInteger, ForeignKey("device_motions.id"))
    device_1hz_motion_id: Mapped[Optional[int]] = mapped_column("device_1hz_motion_id", BigInteger, ForeignKey("device_1hz_motions.id"))
    medication_event_id: Mapped[Optional[int]] = mapped_column("medication_event_id", BigInteger, ForeignKey("medication_events.id"))


    def __repr__(self) -> str:
        return f"<Alert id={self.id} >"
