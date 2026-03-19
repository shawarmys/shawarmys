from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class IntegrationMappings(Base):
    __tablename__ = "integration_mappings"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", ForeignKey("cases.id"))
    lab_results_id: Mapped[Optional[int]] = mapped_column("lab_results_id", ForeignKey("lab_results.id"))
    icd10_data_id: Mapped[Optional[int]] = mapped_column("icd10_data_id", ForeignKey("icd10_data.id"))
    nursing_daily_reports_id: Mapped[Optional[int]] = mapped_column("nursing_daily_reports_id", ForeignKey("nursing_daily_reports.id"))
    medication_events_id: Mapped[Optional[int]] = mapped_column("medication_events_id", ForeignKey("medication_events.id"))
    device_motions_id: Mapped[Optional[int]] = mapped_column("device_motions_id", ForeignKey("device_motions.id"))
    device_1hz_motions_id: Mapped[Optional[int]] = mapped_column("device_1hz_motions_id", ForeignKey("device_1hz_motions.id"))

    def __repr__(self) -> str:
        return f"<NursingDailyReportsData id={self.id} case_id={self.case_id}>"
