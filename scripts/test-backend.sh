#!/usr/bin/env bash
set -euo pipefail

BACKEND_DIR="$(cd "$(dirname "$0")/../backend" && pwd)"

echo "==> Running backend tests..."
cd "$BACKEND_DIR"

# Install dependencies if needed
if [ ! -f ".venv/bin/python" ] && [ ! -f ".venv/Scripts/python.exe" ]; then
  echo "==> Installing backend dependencies..."
  uv sync
fi

# Check if pytest is available, if not install it
if ! uv run python -c "import pytest" 2>/dev/null; then
  echo "==> Installing pytest for testing..."
  uv add --dev pytest pytest-asyncio httpx
fi

echo "==> Running pytest..."
uv run pytest tests -v

echo "==> Backend tests completed successfully!"
