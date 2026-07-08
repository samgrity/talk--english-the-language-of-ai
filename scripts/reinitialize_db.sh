#!/usr/bin/env bash
set -euo pipefail

CONFIRM_FLAG="--confirm-reinitialize-db"

if [[ "${1:-}" != "$CONFIRM_FLAG" ]]; then
  echo "Refusing to reinitialize database without explicit confirmation."
  echo "This operation wipes existing backend database data and reseeds demo data."
  echo "Run: scripts/reinitialize_db.sh $CONFIRM_FLAG"
  exit 1
fi

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/.." && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"

cd "$BACKEND_DIR"
uv run python ../scripts/db/reinitialize_db.py
