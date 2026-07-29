#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$BACKEND_DIR/requirements.txt"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    (cd "$FRONTEND_DIR" && npm install)
fi

# First run trains the world model before serving (see app/main.py's
# lifespan) so this can take up to ~30s the very first time; later runs
# just load the cached checkpoint and start immediately.
(cd "$BACKEND_DIR" && exec "$VENV_DIR/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8000 --reload) &
UVICORN_PID=$!

cleanup() {
    kill "$UVICORN_PID" 2>/dev/null || true
    wait "$UVICORN_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

(cd "$FRONTEND_DIR" && npm run dev)
