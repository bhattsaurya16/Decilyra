"""add CSV ingestion and profiling tables

Revision ID: 0002_csv_ingestion
Revises: 0001_workspaces
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_csv_ingestion"
down_revision: Union[str, Sequence[str], None] = "0001_workspaces"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("data_sources", sa.Column("id", sa.String(36), primary_key=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("source_type", sa.String(32), nullable=False), sa.Column("original_filename", sa.String(255), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("datasets", sa.Column("id", sa.String(36), primary_key=True), sa.Column("source_id", sa.String(36), sa.ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False, unique=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("dataset_versions", sa.Column("id", sa.String(36), primary_key=True), sa.Column("dataset_id", sa.String(36), sa.ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False), sa.Column("version_number", sa.Integer, nullable=False), sa.Column("storage_key", sa.String(255), nullable=False), sa.Column("file_size", sa.Integer, nullable=False), sa.Column("row_count", sa.Integer, nullable=False), sa.Column("column_count", sa.Integer, nullable=False), sa.Column("duplicate_row_count", sa.Integer, nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("dataset_id", "version_number"))
    op.create_index("ix_dataset_versions_dataset_id", "dataset_versions", ["dataset_id"])
    op.create_table("source_columns", sa.Column("id", sa.String(36), primary_key=True), sa.Column("version_id", sa.String(36), sa.ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("position", sa.Integer, nullable=False), sa.Column("inferred_type", sa.String(32), nullable=False), sa.Column("generic_role", sa.String(40), nullable=False), sa.UniqueConstraint("version_id", "position"))
    op.create_index("ix_source_columns_version_id", "source_columns", ["version_id"])
    op.create_table("field_profiles", sa.Column("id", sa.String(36), primary_key=True), sa.Column("column_id", sa.String(36), sa.ForeignKey("source_columns.id", ondelete="CASCADE"), nullable=False, unique=True), sa.Column("null_count", sa.Integer, nullable=False), sa.Column("null_percentage", sa.Float, nullable=False), sa.Column("unique_count", sa.Integer, nullable=False), sa.Column("numeric_min", sa.Float), sa.Column("numeric_max", sa.Float), sa.Column("numeric_mean", sa.Float), sa.Column("date_min", sa.String(64)), sa.Column("date_max", sa.String(64)), sa.Column("sample_values", sa.JSON, nullable=False))
    op.create_table("quality_issues", sa.Column("id", sa.String(36), primary_key=True), sa.Column("version_id", sa.String(36), sa.ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False), sa.Column("column_name", sa.String(255)), sa.Column("code", sa.String(64), nullable=False), sa.Column("severity", sa.String(16), nullable=False), sa.Column("message", sa.Text, nullable=False), sa.Column("details", sa.JSON, nullable=False))
    op.create_index("ix_quality_issues_version_id", "quality_issues", ["version_id"])


def downgrade() -> None:
    op.drop_index("ix_quality_issues_version_id", table_name="quality_issues")
    op.drop_table("quality_issues")
    op.drop_table("field_profiles")
    op.drop_index("ix_source_columns_version_id", table_name="source_columns")
    op.drop_table("source_columns")
    op.drop_index("ix_dataset_versions_dataset_id", table_name="dataset_versions")
    op.drop_table("dataset_versions")
    op.drop_table("datasets")
    op.drop_table("data_sources")
