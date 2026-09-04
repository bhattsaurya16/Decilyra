# Roadmap

## Phase 1 — Foundation

Repository layout, local development, frontend shell, landing page, FastAPI skeleton, database-ready configuration, documentation.

## Phase 2 — CSV ingestion

**Complete.** Secure CSV upload, replaceable local storage, dataset/version metadata, schema discovery, deterministic column profiles, quality checks, source listing, dataset detail, and bounded preview. No analytics or canonical business mapping.

## Phase 3 — Semantic mapping

**Complete.** Seed a stable MVP canonical catalog, generate deterministic version-bound suggestions with evidence and product-confidence levels, handle ambiguity, and persist confirmation, override, rejection, and unmapped decisions.

## Phase 4 — Data quality

Extend the foundational Phase 2 checks with workspace-configurable policies, remediation workflows, and mapping-aware blockers before methods run.

## Phase 5 — Method registry

Catalog allowed methods, inputs, outputs, and preconditions. Governance before computation.

## Phase 6 — Eligibility engine

Given mapped, quality-checked data, decide which methods are valid.

## Phase 7 — Analytics engine

Execute eligible methods deterministically in Python.

## Phase 8 — Dashboard integration

Replace illustrative demo series with API-backed KPIs and charts.

## Phase 9 — Findings

Turn method outputs into inspectable claims with lineage.

## Phase 10 — Ask Decilyra

Connect the chat shell to an OpenAI-compatible provider that only reasons over validated results.

## Phase 11 — Scenario Lab

Clone a baseline, apply assumptions, compute deltas.

## Phase 12 — PostgreSQL connector

Ingest from hosted Postgres / Supabase in addition to CSV.

## Phase 13 — Decision Lab

Compare options against evidence and scenarios.

## Phase 14 — Deployment hardening

Production auth, secrets, observability, and environment promotion on Vercel plus Render or Railway.
