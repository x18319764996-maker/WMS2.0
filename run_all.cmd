@echo off
REM Run all configured UI automation scenarios on Windows.
setlocal

cd /d %~dp0

if not defined ENABLE_LIVE_UI set ENABLE_LIVE_UI=true
if not defined TEST_ENV set TEST_ENV=test
if not defined AI_MODE set AI_MODE=disabled
if not defined HEADLESS set HEADLESS=false

python -m uv run run-all-scenarios %*

endlocal
