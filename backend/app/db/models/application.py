from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ApplicationModel(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    mobile: Mapped[str] = mapped_column(String(40), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=False)
    current_role: Mapped[str] = mapped_column(String(100), nullable=False)
    seniority_level: Mapped[str] = mapped_column(String(40), nullable=False)
    job_title: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[str] = mapped_column(String(20), nullable=False)
    sub_departments: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), nullable=False)
    assignee_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    screening_status: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    locale_country: Mapped[str] = mapped_column(String(10), nullable=False)
    locale_preferred_language: Mapped[str] = mapped_column(String(20), nullable=False)
    locale_region: Mapped[str] = mapped_column(String(20), nullable=False)
    locale_store_id: Mapped[str] = mapped_column(String(20), nullable=False)

    company = relationship("CompanyModel", back_populates="applications")
    updates = relationship("UpdateModel", back_populates="application", order_by="UpdateModel.timestamp")
