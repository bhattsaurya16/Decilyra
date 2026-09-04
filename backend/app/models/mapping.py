from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.dataset import new_id


class CanonicalField(Base):
    __tablename__ = "canonical_fields"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    domain: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    expected_data_type: Mapped[str] = mapped_column(String(32), nullable=False)
    expected_grain: Mapped[str] = mapped_column(String(40), default="UNKNOWN", nullable=False)
    unit_type: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(40), nullable=False)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    examples: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class FieldMapping(Base):
    __tablename__ = "field_mappings"
    __table_args__ = (UniqueConstraint("dataset_version_id", "source_column_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_version_id: Mapped[str] = mapped_column(ForeignKey("dataset_versions.id", ondelete="CASCADE"), index=True, nullable=False)
    source_column_id: Mapped[str] = mapped_column(ForeignKey("source_columns.id", ondelete="CASCADE"), index=True, nullable=False)
    canonical_field_id: Mapped[str | None] = mapped_column(ForeignKey("canonical_fields.id"), index=True)
    status: Mapped[str] = mapped_column(String(24), default="UNMAPPED", nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)
    confidence_level: Mapped[str | None] = mapped_column(String(16))
    mapping_method: Mapped[str] = mapped_column(String(16), default="HEURISTIC", nullable=False)
    evidence: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    alternatives: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list, nullable=False)
    confirmed_by_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    grain: Mapped[str] = mapped_column(String(40), default="UNKNOWN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    source_column = relationship("SourceColumn")
    canonical_field = relationship("CanonicalField")
    dataset_version = relationship("DatasetVersion")
