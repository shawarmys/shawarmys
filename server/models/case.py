from datetime import date
from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column("patient_id", BigInteger, nullable=False)
    admission_date: Mapped[Optional[date]] = mapped_column("admission_date", Date)
    discharge_date: Mapped[Optional[date]] = mapped_column("discharge_date", Date)

    def __repr__(self) -> str:
        return f"<Case id={self.id} patient_id={self.patient_id}>"
