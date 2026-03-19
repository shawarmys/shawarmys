import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Files(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", String(512), nullable=False)
    group_type: Mapped[str] = mapped_column("group_type", String(256), nullable=False)
    source: Mapped[str] = mapped_column("source", String(256), nullable=False)
    entries: Mapped[int] = mapped_column("entries", Integer, nullable=False)
    records: Mapped[int] = mapped_column("records", Integer, nullable=False)
    type: Mapped[str] = mapped_column("type", String(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at",
        DateTime,
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )

    def __repr__(self) -> str:
        return (
            f"<Files id={self.id} name={self.name} source={self.source} "
            f"group_type={self.group_type} "
            f"entries={self.entries} records={self.records} type={self.type}>"
        )
