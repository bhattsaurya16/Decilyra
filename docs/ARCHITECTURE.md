# Architecture

## Current (Phase 3)

```text
Browser
→ Next.js frontend
→ FastAPI API
→ PostgreSQL
```

The frontend is a Next.js App Router application. It talks to FastAPI through a centralized client in `frontend/src/lib/api`. The backend exposes versioned routes under `/api/v1`. CSV ingestion requires a configured database; Alembic owns the relational schema.

```text
frontend/          Next.js, TypeScript, Tailwind, shadcn/ui
backend/           FastAPI, Pydantic, SQLAlchemy, Alembic
database/          local Postgres notes and compose service
```

AI providers, analytics libraries, and connectors are intentionally absent from the runtime path.

## CSV ingestion path

```text
multipart CSV upload
→ extension and byte-limit validation
→ UTF-8 CSV parse
→ deterministic schema/profile/quality pass
→ generated-key storage adapter
→ transactional metadata persistence
→ bounded preview read (1–100 rows)
```

`data_sources` owns connection-level metadata. A source owns one `datasets` record, which owns immutable `dataset_versions`. Each version owns ordered `source_columns`, one `field_profiles` record per column, and its `quality_issues`. Local files are referenced only by opaque generated storage keys. The `StorageService` interface is the seam for a later Supabase Storage adapter.

Profiling assigns only structural types and generic candidate roles. It does not assign business semantics such as `NET_REVENUE`.

## Canonical semantic layer

```text
Dataset → immutable Dataset Version → Source Column
→ version-bound Field Mapping → stable Canonical Field
```

The canonical catalog is defined once in `backend/app/domain/canonical_fields/catalog.py` and seeded by Alembic. Codes are stable contracts intended for future Method Registry input declarations. Catalog entries carry domain, definition, expected type and grain, unit type, entity type, and aliases. Currency-valued fields never imply USD or another currency.

The deterministic mapper combines normalized names and aliases, profile type/role compatibility, numeric ranges where relevant, and related-field context. Each suggestion stores its score, High/Medium/Low product-confidence label, evidence, and alternatives. The score ranks deterministic support; it is not a statistical probability, model confidence, or probability of truth.

Definition-sensitive concepts remain `NEEDS_REVIEW`. For example, `sales_amount` can suggest `NET_REVENUE`, but profiling cannot establish whether discounts, returns, and allowances are already deducted. User actions are explicit and persisted: confirm, override, reject, or unmapped. Re-running suggestions does not overwrite reviewed mappings.

Mappings belong to a dataset version. A new version receives new suggestions; prior confirmations are retained for audit and are never silently applied to renamed columns. Reuse suggestions can be added later with explicit evidence.

The attached analytical Method Registry workbook informed stable terminology and definition boundaries only. Phase 3 does not ingest or execute its methods.

## Future

```text
Data Sources
→ Profiling
→ Semantic Mapping
→ Eligibility Engine
→ Method Engine
→ Findings
→ Scenarios
→ AI Interface
```

### Data sources

CSV is implemented. PostgreSQL connectors and additional sources remain future work. Ingestion writes metadata and profiles; it does not compute business results.

### Profiling and mapping

Python services inspect schemas and values. Semantic mapping assigns meaning. Quality checks gate eligibility.

### Eligibility and methods

The method registry declares preconditions. The eligibility engine decides what may run. The method engine executes deterministic analytics (Pandas / NumPy / SciPy / statsmodels as needed).

### Findings, scenarios, decisions

Findings are structured claims with lineage. Scenarios clone a baseline. Decision Lab compares options. None of these should be implemented as prompt-only logic.

### AI interface

Ask Decilyra consumes validated outputs. Provider access should stay behind a backend abstraction (OpenAI-compatible), never in the browser.

## Deployment target

- Frontend: Vercel
- Backend: Render or Railway
- Database: PostgreSQL, later Supabase-hosted
