# Decilyra

**From data to defensible decisions.**

Decilyra is a business decision-intelligence platform. It connects to company data, determines which analytical methods are valid, performs deterministic analysis, generates findings, supports scenario modeling, and provides an AI conversational interface over validated results.

AI explains. It does not invent the number.

## Architecture

```text
Browser → Next.js frontend → FastAPI API → PostgreSQL
```

Future path:

```text
Data Sources → Profiling → Semantic Mapping → Eligibility Engine → Method Engine → Findings → Scenarios → AI Interface
```

Roles:

- Python = truth engine
- SQL = data engine
- Method Registry = governance engine
- AI = conversational reasoning interface

## Current phase

**Phase 3 — Semantic business field mapping.** Profiled columns receive deterministic canonical-field suggestions with evidence and product-confidence levels. Users can confirm, override, reject, or leave mappings unmapped. Every mapping remains bound to its source column and dataset version. No method execution, analytics, or AI mapping is included.

## Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js, TypeScript, React, Tailwind CSS, shadcn/ui, Recharts |
| Backend | FastAPI, Python, Pydantic, SQLAlchemy, Alembic |
| Data | PostgreSQL (optional locally; Supabase later) |
| Deploy | Vercel (frontend), Render or Railway (backend) |

## Repository structure

```text
decilyra/
├── frontend/          Next.js application
├── backend/           FastAPI application
├── docs/              Product, architecture, roadmap
├── database/          Postgres notes
├── scripts/           Local helper scripts
├── .github/           CI
├── docker-compose.yml Local PostgreSQL
└── README.md
```

## Local setup

Requirements: Node.js 20+, Python 3.12+ (3.14 is fine), and optionally Docker for PostgreSQL.

```bash
git clone <repository-url>
cd Decilyra
```

### Frontend

```bash
cd frontend
copy .env.example .env.local   # Windows
# cp .env.example .env.local  # macOS / Linux
npm install
npm run dev
```

The app runs at [http://localhost:3000](http://localhost:3000).

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
copy .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)  
Docs (development): [http://localhost:8000/docs](http://localhost:8000/docs)

Helper scripts:

```bash
# from repository root, PowerShell
.\scripts\dev-backend.ps1
.\scripts\dev-frontend.ps1
```

```bash
# macOS / Linux
./scripts/dev-backend.sh
./scripts/dev-frontend.sh
```

## Environment configuration

`frontend/.env.example`

```text
NEXT_PUBLIC_API_URL=http://localhost:8000
```

`backend/.env.example`

```text
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://decilyra:decilyra@localhost:5432/decilyra
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
MAX_UPLOAD_SIZE_MB=25
UPLOAD_DIR=storage/uploads
```

Never commit `.env` files with secrets.

## Database notes

PostgreSQL is not required to render the UI or to hit `/api/v1/health`.

To run a local database:

```bash
docker compose up -d postgres
cd backend
alembic upgrade head
```

Supabase: create a project later, then set `DATABASE_URL` to the SQLAlchemy form of the connection string (`postgresql+psycopg://...`). See `database/README.md`.

## Test the sample CSV

After starting PostgreSQL and applying migrations, start both applications and open [http://localhost:3000/data/sources](http://localhost:3000/data/sources). Drag `samples/demo_sales.csv` into the upload area. Select the created source to inspect its profile, then choose **Open field mapping**. Review the evidence for each suggestion and confirm, change, reject, or leave fields unmapped. The sample intentionally keeps revenue and discount meanings reviewable because profiling cannot prove their accounting definitions.

Uploaded content is written to `backend/storage/uploads` by default. The directory is excluded from Git and storage keys are never returned by the API.

## Testing

Frontend:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

Backend:

```bash
cd backend
pytest
```

## Roadmap

Phases 1–14 are listed in [docs/ROADMAP.md](docs/ROADMAP.md). The next intended slice is **Phase 4 — expanded data quality policy and remediation**.

## Deployment target

- Frontend on Vercel
- Backend on Render or Railway
- PostgreSQL via Supabase or the host’s managed Postgres

Production secrets (Supabase URI, AI provider keys, auth) are not required for Phase 3.
