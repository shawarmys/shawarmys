from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Icd10Data(Base):
    __tablename__ = "icd10_data"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", ForeignKey("cases.id"))
    patient_id: Mapped[Optional[int]] = mapped_column("patient_id", BigInteger)
    ward: Mapped[Optional[str]] = mapped_column("ward", String(256))
    admission_date: Mapped[Optional[Date]] = mapped_column("admission_date", Date)
    discharge_date: Mapped[Optional[Date]] = mapped_column("discharge_date", Date)
    length_of_stay_days: Mapped[Optional[int]] = mapped_column("length_of_stay_days", Integer)
    primary_icd10_code: Mapped[Optional[str]] = mapped_column("primary_icd10_code", String(256))
    primary_icd10_description_en: Mapped[Optional[str]] = mapped_column("primary_icd10_description_en", String(256))
    secondary_icd10_codes: Mapped[Optional[str]] = mapped_column("secondary_icd10_codes", String(256))
    secondary_icd10_descriptions_en: Mapped[Optional[str]] = mapped_column("secondary_icd10_descriptions_en", String(256))
    ops_codes: Mapped[Optional[str]] = mapped_column("ops_codes", String(256))
    ops_descriptions_en: Mapped[Optional[str]] = mapped_column("ops_descriptions_en", String(256))

    def __repr__(self) -> str:
        return f"<Icd10Data id={self.id} case_id={self.case_id}>"
