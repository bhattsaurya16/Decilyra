# Product specification

## Name

Decilyra

## Tagline

From data to defensible decisions.

## Vision

Decilyra is a business decision-intelligence platform. It connects to company data, determines which analytical methods are valid, performs deterministic analysis, generates findings, supports scenario modeling, and provides an AI conversational interface over validated analytical results.

It is not a generic chatbot over a warehouse. Analysis happens first. Conversation happens second.

## Operating principle

```text
Business Data
→ Data Understanding
→ Quality
→ Semantic Mapping
→ Method Eligibility
→ Deterministic Analytics
→ Findings
→ Scenarios
→ Decisions
→ AI Explanation
```

## Engine roles

- **Python** is the truth engine.
- **SQL** is the data engine.
- **Method Registry** is the governance engine.
- **AI** is the conversational reasoning interface.

## Users

Operators, finance partners, and leadership who must defend a number: why it moved, whether the method was allowed, and what happens if an assumption changes.

## Phase 1 scope

Foundation only: repository, local development, application shell, public landing page, FastAPI skeleton, PostgreSQL-ready configuration, API client, and documentation.

Phase 1 does not ingest data, run methods, authenticate users, or call an AI provider.
