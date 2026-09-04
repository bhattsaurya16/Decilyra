from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def new_id() -> str:
    return str(uuid4())


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), default="csv", nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ready", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    dataset: Mapped[Dataset] = relationship(back_populates="source", cascade="all, delete-orphan", uselist=False)


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id", ondelete="CASCADE"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    source: Mapped[DataSource] = relationship(back_populates="dataset")
    versions: Mapped[list[DatasetVersion]] = relationship(back_populates="dataset", cascade="all, delete-orphan")


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"
    __table_args__ = (UniqueConstraint("dataset_id", "version_number"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    dataset_id: Mapped[str] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, nullable=False)
    duplicate_row_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    dataset: Mapped[Dataset] = relationship(back_populates="versions")
    columns: Mapped[list[SourceColumn]] = relationship(back_populates="version", cascade="all, delete-orphan")
    quality_issues: Mapped[list[QualityIssue]] = relationship(back_populates="version", cascade="all, delete-orphan")


class SourceColumn(Base):
    __tablename__ = "source_columns"
    __table_args__ = (UniqueConstraint("version_id", "position"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    version_id: Mapped[str] = mapped_column(ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    inferred_type: Mapped[str] = mapped_column(String(32), nullable=False)
    generic_role: Mapped[str] = mapped_column(String(40), nullable=False)
    version: Mapped[DatasetVersion] = relationship(back_populates="columns")
    profile: Mapped[FieldProfile] = relationship(back_populates="column", cascade="all, delete-orphan", uselist=False)


class FieldProfile(Base):
    __tablename__ = "field_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    column_id: Mapped[str] = mapped_column(ForeignKey("source_columns.id", ondelete="CASCADE"), unique=True, nullable=False)
    null_count: Mapped[int] = mapped_column(Integer, nullable=False)
    null_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    unique_count: Mapped[int] = mapped_column(Integer, nullable=False)
    numeric_min: Mapped[float | None] = mapped_column(Float)
    numeric_max: Mapped[float | None] = mapped_column(Float)
    numeric_mean: Mapped[float | None] = mapped_column(Float)
    date_min: Mapped[str | None] = mapped_column(String(64))
    date_max: Mapped[str | None] = mapped_column(String(64))
    sample_values: Mapped[list[object]] = mapped_column(JSON, default=list, nullable=False)
    column: Mapped[SourceColumn] = relationship(back_populates="profile")


class QualityIssue(Base):
    __tablename__ = "quality_issues"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    version_id: Mapped[str] = mapped_column(ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    column_name: Mapped[str | None] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    version: Mapped[DatasetVersion] = relationship(back_populates="quality_issues")
