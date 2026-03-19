from typing import Optional

from database import Base
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class MedicationEvents(Base):
    __tablename__ = "medication_events"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    record_type: Mapped[Optional[str]] = mapped_column("record_type", String(256))
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", BigInteger)
    encounter_id: Mapped[Optional[str]] = mapped_column("encounter_id", String(256))
    ward: Mapped[Optional[str]] = mapped_column("ward", String(256))
    admission_datetime: Mapped[Optional[str]] = mapped_column("admission_datetime", String(256))
    discharge_datetime: Mapped[Optional[str]] = mapped_column("discharge_datetime", String(256))
    order_id: Mapped[Optional[str]] = mapped_column("order_id", String(256))
    order_uuid: Mapped[Optional[str]] = mapped_column("order_uuid", String(256))
    medication_code_atc: Mapped[Optional[str]] = mapped_column("medication_code_atc", String(256))
    medication_name: Mapped[Optional[str]] = mapped_column("medication_name", String(256))
    route: Mapped[Optional[str]] = mapped_column("route", String(256))
    dose: Mapped[Optional[str]] = mapped_column("dose", String(256))
    dose_unit: Mapped[Optional[str]] = mapped_column("dose_unit", String(256))
    frequency: Mapped[Optional[str]] = mapped_column("frequency", String(256))
    order_start_datetime: Mapped[Optional[str]] = mapped_column("order_start_datetime", String(256))
    order_stop_datetime: Mapped[Optional[str]] = mapped_column("order_stop_datetime", String(256))
    is_prn_0_1: Mapped[Optional[str]] = mapped_column("is_prn_0_1", String(256))
    indication: Mapped[Optional[str]] = mapped_column("indication", String(256))
    prescriber_role: Mapped[Optional[str]] = mapped_column("prescriber_role", String(256))
    order_status: Mapped[Optional[str]] = mapped_column("order_status", String(256))
    administration_datetime: Mapped[Optional[str]] = mapped_column("administration_datetime", String(256))
    administered_dose: Mapped[Optional[str]] = mapped_column("administered_dose", String(256))
    administered_unit: Mapped[Optional[str]] = mapped_column("administered_unit", String(256))
    administration_status: Mapped[Optional[str]] = mapped_column("administration_status", String(256))
    note: Mapped[Optional[str]] = mapped_column("note", String(256))

    def __repr__(self) -> str:
        return f"<MedicationInpatientData id={self.id} patient_id={self.patient_id}>"
