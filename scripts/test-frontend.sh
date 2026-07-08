#!/usr/bin/env bash
set -euo pipefail

FRONTEND_DIR="$(cd "$(dirname "$0")/../frontend" && pwd)"

echo "==> Running frontend tests..."
cd "$FRONTEND_DIR"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "==> Installing frontend dependencies..."
  npm install
fi

# Run tests with coverage
echo "==> Running Jest test suite with coverage..."
npm test -- --coverage --watchAll=false

echo "==> Running TypeScript type checking on application code..."
npx tsc --noEmit

echo "==> Running Next.js build test..."
npm run build

echo "==> Frontend tests completed successfully!"