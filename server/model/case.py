from database import Base
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column("patient_id", ForeignKey("patients.id"), nullable=False)


    def __repr__(self) -> str:
        return f"<Case id={self.id} patient_id={self.patient_id}>"
