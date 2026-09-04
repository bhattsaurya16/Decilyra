#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../backend"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
fi
.venv/bin/uvicorn app.main:app --reload --port 8000
