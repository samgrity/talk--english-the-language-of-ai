#!/usr/bin/env bash
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/.." && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"
FRONTEND_DIR="$REPO_ROOT/frontend"
BACKEND_PORT=8000
FRONTEND_PORT=3000

port_pid() {
  lsof -i :"$1" -sTCP:LISTEN -t 2>/dev/null || true
}

stop_port_if_running() {
  local port=$1
  local name=$2
  local pid
  pid=$(port_pid "$port")

  if [[ -n "$pid" ]]; then
    echo "$name already running on port $port (pid: $pid). Restarting..."
    kill "$pid" 2>/dev/null || true
    sleep 1

    pid=$(port_pid "$port")
    if [[ -n "$pid" ]]; then
      echo "$name still running on port $port (pid: $pid). Forcing stop..."
      kill -9 "$pid" 2>/dev/null || true
      sleep 1
    fi
  fi
}

ensure_backend_deps() {
  if [[ ! -f "$BACKEND_DIR/.venv/bin/python" && ! -f "$BACKEND_DIR/.venv/Scripts/python.exe" ]]; then
    echo "==> Installing backend dependencies..."
    (cd "$BACKEND_DIR" && uv sync)
  else
    echo "==> Backend dependencies already installed"
  fi
}

ensure_frontend_deps() {
  if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    echo "==> Installing frontend dependencies..."
    (cd "$FRONTEND_DIR" && npm install)
  else
    echo "==> Frontend dependencies already installed"
  fi
}

cleanup() {
  echo ""
  echo "Shutting down development servers..."
  if [[ -n "${BACKEND_PID:-}" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "${FRONTEND_PID:-}" ]]; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
  wait 2>/dev/null || true
}

echo "==> Ensuring ports are clear"
stop_port_if_running "$BACKEND_PORT" "Backend"
stop_port_if_running "$FRONTEND_PORT" "Frontend"

ensure_backend_deps
ensure_frontend_deps

echo "==> Starting backend on port $BACKEND_PORT"
(cd "$BACKEND_DIR" && uv run uvicorn main:app --reload --port "$BACKEND_PORT") 2>&1 | sed 's/^/[backend] /' &
BACKEND_PID=$!

echo "==> Starting frontend on port $FRONTEND_PORT"
(cd "$FRONTEND_DIR" && npm run dev) 2>&1 | sed 's/^/[frontend] /' &
FRONTEND_PID=$!

trap cleanup EXIT INT TERM

wait "$BACKEND_PID" "$FRONTEND_PID"
