from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Files(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    file_type: Mapped[str] = mapped_column("file_type", String(256), nullable=False)
    origin_type: Mapped[str] = mapped_column("origin_type", String(256), nullable=False)

    def __repr__(self) -> str:
        return f"<Files id={self.id} file_type={self.file_type} origin_type={self.origin_type}>"
