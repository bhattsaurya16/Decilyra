"""add canonical fields and version-bound mappings

Revision ID: 0003_semantic_mapping
Revises: 0002_csv_ingestion
"""
from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from app.domain.canonical_fields.catalog import CANONICAL_FIELDS

revision: str = "0003_semantic_mapping"
down_revision: Union[str, Sequence[str], None] = "0002_csv_ingestion"
branch_labels = None
depends_on = None


def upgrade() -> None:
    canonical = op.create_table(
        "canonical_fields",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False, unique=True),
        sa.Column("domain", sa.String(32), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.String(1000), nullable=False),
        sa.Column("expected_data_type", sa.String(32), nullable=False),
        sa.Column("expected_grain", sa.String(40), nullable=False),
        sa.Column("unit_type", sa.String(32), nullable=False),
        sa.Column("entity_type", sa.String(40), nullable=False),
        sa.Column("aliases", sa.JSON, nullable=False),
        sa.Column("examples", sa.JSON, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_canonical_fields_code", "canonical_fields", ["code"], unique=True)
    op.create_index("ix_canonical_fields_domain", "canonical_fields", ["domain"])
    op.create_table(
        "field_mappings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dataset_version_id", sa.String(36), sa.ForeignKey("dataset_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_column_id", sa.String(36), sa.ForeignKey("source_columns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("canonical_field_id", sa.String(36), sa.ForeignKey("canonical_fields.id")),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("confidence", sa.Float),
        sa.Column("confidence_level", sa.String(16)),
        sa.Column("mapping_method", sa.String(16), nullable=False),
        sa.Column("evidence", sa.JSON, nullable=False),
        sa.Column("alternatives", sa.JSON, nullable=False),
        sa.Column("confirmed_by_user", sa.Boolean, nullable=False),
        sa.Column("grain", sa.String(40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("dataset_version_id", "source_column_id"),
    )
    op.create_index("ix_field_mappings_dataset_version_id", "field_mappings", ["dataset_version_id"])
    op.create_index("ix_field_mappings_source_column_id", "field_mappings", ["source_column_id"])
    op.create_index("ix_field_mappings_canonical_field_id", "field_mappings", ["canonical_field_id"])
    now = datetime.now(timezone.utc)
    op.bulk_insert(canonical, [{"id": str(uuid4()), **definition, "examples": [], "active": True, "created_at": now, "updated_at": now} for definition in CANONICAL_FIELDS])


def downgrade() -> None:
    op.drop_index("ix_field_mappings_canonical_field_id", table_name="field_mappings")
    op.drop_index("ix_field_mappings_source_column_id", table_name="field_mappings")
    op.drop_index("ix_field_mappings_dataset_version_id", table_name="field_mappings")
    op.drop_table("field_mappings")
    op.drop_index("ix_canonical_fields_domain", table_name="canonical_fields")
    op.drop_index("ix_canonical_fields_code", table_name="canonical_fields")
    op.drop_table("canonical_fields")
