from typing import Optional

from database import Base
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class NursingDailyReports(Base):
    __tablename__ = "nursing_daily_reports"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", ForeignKey("cases.id"))
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", ForeignKey("patients.id"))
    ward: Mapped[Optional[str]] = mapped_column("ward", String(256))
    report_date: Mapped[Optional[str]] = mapped_column("report_date", String(256))
    shift: Mapped[Optional[str]] = mapped_column("shift", String(256))
    nursing_note_free_text: Mapped[Optional[str]] = mapped_column("nursing_note_free_text", String(256))

    def __repr__(self) -> str:
        return f"<NursingDailyReportsData id={self.id} case_id={self.case_id}>"
