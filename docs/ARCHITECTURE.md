# Architecture

## Current (Phase 1)

```text
Browser
→ Next.js frontend
→ FastAPI API
→ PostgreSQL
```

The frontend is a Next.js App Router application. It talks to FastAPI through a single client in `frontend/src/lib/api`. The backend exposes versioned routes under `/api/v1`. PostgreSQL is optional for local UI work; Alembic and SQLAlchemy are wired so persistence can be enabled with `DATABASE_URL`.

```text
frontend/          Next.js, TypeScript, Tailwind, shadcn/ui
backend/           FastAPI, Pydantic, SQLAlchemy, Alembic
database/          local Postgres notes and compose service
```

AI providers, analytics libraries, and connectors are intentionally absent from the runtime path.

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

CSV first, then PostgreSQL (including Supabase) and additional connectors. Ingestion writes into the data engine; it does not compute business results.

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
