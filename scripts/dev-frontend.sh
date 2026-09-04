#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../frontend"
if [ ! -f .env.local ]; then
  cp .env.example .env.local
fi
npm install
npm run dev
