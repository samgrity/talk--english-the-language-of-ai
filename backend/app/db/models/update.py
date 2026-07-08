from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UpdateModel(Base):
    __tablename__ = "updates"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    application_id: Mapped[str] = mapped_column(ForeignKey("applications.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actor: Mapped[str] = mapped_column(String(40), nullable=False)
    internal_notes: Mapped[str] = mapped_column(Text, nullable=False)
    recruiter_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    update_type: Mapped[str] = mapped_column(String(40), nullable=False)
    correspondence: Mapped[str | None] = mapped_column(Text, nullable=True)

    application = relationship("ApplicationModel", back_populates="updates")
