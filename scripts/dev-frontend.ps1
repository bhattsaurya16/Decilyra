$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\frontend"
if (-not (Test-Path .env.local)) {
  Copy-Item .env.example .env.local
}
npm install
npm run dev
