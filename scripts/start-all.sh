#!/usr/bin/env bash
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/.." && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"
FRONTEND_DIR="$REPO_ROOT/frontend"
BACKEND_PORT=8000
FRONTEND_PORT=3000

port_pid() {
  lsof -tiTCP:"$1" 2>/dev/null || true
}

kill_tree() {
  local pid=$1
  local child

  for child in $(pgrep -P "$pid" 2>/dev/null || true); do
    kill_tree "$child"
  done

  kill "$pid" 2>/dev/null || true
}

stop_port_if_running() {
  local port=$1
  local name=$2
  local pids
  pids=$(port_pid "$port")

  if [[ -n "$pids" ]]; then
    echo "$name already has processes attached to port $port (pid: ${pids//$'\n'/, }). Restarting..."
    for pid in $pids; do
      kill_tree "$pid"
    done
    sleep 1

    pids=$(port_pid "$port")
    if [[ -n "$pids" ]]; then
      echo "$name still has processes attached to port $port (pid: ${pids//$'\n'/, }). Forcing stop..."
      for pid in $pids; do
        kill -9 "$pid" 2>/dev/null || true
      done
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
    kill_tree "$BACKEND_PID"
  fi
  if [[ -n "${FRONTEND_PID:-}" ]]; then
    kill_tree "$FRONTEND_PID"
  fi
  wait 2>/dev/null || true
}

echo "==> Ensuring ports are clear"
stop_port_if_running "$BACKEND_PORT" "Backend"
stop_port_if_running "$FRONTEND_PORT" "Frontend"

ensure_backend_deps
ensure_frontend_deps

echo "==> Starting backend on port $BACKEND_PORT"
(cd "$BACKEND_DIR" && uv run python -m uvicorn main:app --reload --port "$BACKEND_PORT") \
  > >(sed 's/^/[backend] /') \
  2> >(sed 's/^/[backend] /' >&2) &
BACKEND_PID=$!

echo "==> Starting frontend on port $FRONTEND_PORT"
(cd "$FRONTEND_DIR" && npm run dev) \
  > >(sed 's/^/[frontend] /') \
  2> >(sed 's/^/[frontend] /' >&2) &
FRONTEND_PID=$!

trap cleanup EXIT INT TERM

wait "$BACKEND_PID" "$FRONTEND_PID"
