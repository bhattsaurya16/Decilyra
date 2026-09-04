# Database foundation

Decilyra uses PostgreSQL as the system-of-record database.

## Local development

The easiest local option is Docker Compose from the repository root:

```bash
docker compose up -d postgres
```

Then copy `backend/.env.example` to `backend/.env`. The default URL is:

```text
postgresql+psycopg://decilyra:decilyra@localhost:5432/decilyra
```

Run migrations from `backend/`:

```bash
alembic upgrade head
```

Docker is optional. You can point `DATABASE_URL` at any local PostgreSQL instance.

The API starts without a database. Persistence endpoints will return `503` until `DATABASE_URL` is set.

## Supabase (later)

When you are ready to use hosted Postgres:

1. Create a Supabase project.
2. Copy the URI from Project Settings → Database.
3. Set `DATABASE_URL` to the pooled or direct connection string, using the SQLAlchemy driver prefix:

```text
postgresql+psycopg://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

Never commit the password. Keep it in environment variables or a secret manager.

Phase 1 does not require a production Supabase project.
