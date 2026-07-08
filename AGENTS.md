# AGENTS.md
Guide for coding agents in `hireflow`.

## Scope and rule sources
- Applies to the full repository.
- No Cursor rules found: `.cursorrules` and `.cursor/rules/` are absent.
- No Copilot rules found: `.github/copilot-instructions.md` is absent.
- If those files appear later, follow them as higher-priority instructions.

## Operator updates (Mac terminal)
- For major tasks, announce progress with the macOS `say` command using a short phrase.
- Keep updates brief (for example: `say "Updating frontend tests"`).
- When all requested work is fully complete, run a final spoken completion notice.
- Final notice example: `say "Task complete, please check terminal"`.

## Repository map
- `frontend/`: Next.js 15 + React 19 + TypeScript.
- `backend/`: FastAPI app with mock data for now (will change soon).
- `scripts/`: service start/test orchestration plus seed-data utilities (`retrieve_linked_in.py`, `review_from_seed_data.py`).
- Root `package.json`: contains Playwright dependency only.

## Tooling facts
- Frontend package manager: `npm`.
- Backend package manager/runtime: `uv`.
- Frontend tests: Jest + React Testing Library.
- Backend tests: pytest + `fastapi.testclient.TestClient`.
- TypeScript strict mode is enabled in `frontend/tsconfig.json`.
- Frontend alias: `@/*` resolves to `frontend/*`.

## Install dependencies
```bash
cd frontend && npm install
cd backend && uv sync
```

## Run services
```bash
# from repo root
./scripts/start-all.sh
```

Manual run:
```bash
cd backend && uv run uvicorn main:app --reload --port 8000
cd frontend && npm run dev
```

## Build/lint/test commands

### Frontend (`frontend/`)
```bash
npm run dev
npm run build
npm test
npm run test:watch
npm run test:css
npx tsc --noEmit
```

Notes:
- No dedicated ESLint script/config is currently present.
- `./scripts/test-frontend.sh` runs Jest with coverage, `tsc --noEmit`, then `next build`.

### Backend (`backend/`)
```bash
uv run uvicorn main:app --reload --port 8000
uv run pytest test_main.py -v
uv run pytest -v
```

### Whole project
```bash
./scripts/test-all.sh
```

## Running a single test (important)

Frontend single test patterns:
```bash
cd frontend
npm test -- __tests__/components/CandidateTable.test.tsx
npm test -- -t "should navigate to review page when row is clicked"
npm test -- __tests__/components/CandidateTable.test.tsx -t "render table headers"
```

Backend single test patterns:
```bash
cd backend
uv run pytest test_main.py -v
uv run pytest test_main.py::test_get_applications -v
uv run pytest -k "ordering" -v
```

## Code style guidelines
Match existing style in touched files and avoid unrelated reformatting.

### Imports
- Frontend import order: framework/vendor, then `@/...`, then relative imports.
- Prefer `@/` aliases over deep relative paths in frontend code.

### TypeScript and React
- Use functional components and hooks.
- Use explicit prop interfaces/types.
- Keep shared API contracts in `frontend/types/api.ts`.
- Keep backend wire values unchanged.
- Prefer `async/await` over `.then()` chains.
- API helpers should throw `Error` on non-2xx responses.
- UI code should use `try/catch/finally` for loading/error state transitions.
- Naming: components/types in PascalCase, vars/functions in camelCase, hooks start with `use`.

### Formatting
- Keep quote style consistent with the local file.
- Keep semicolon usage consistent with the local file.
- Keep helpers small and focused.
- Add comments only when logic is non-obvious.

### Python and FastAPI
- Use `async def` endpoints and type hints.
- Use Pydantic models for request/response shapes.
- Preserve camelCase payload fields to match frontend contracts.
- Raise `HTTPException` with clear status/detail for errors.
- Keep behavior deterministic for tests.

### Naming conventions
- TS component/type names: PascalCase.
- TS function/variable names: camelCase.
- Python function/local names: snake_case.
- Module-level constants: UPPER_SNAKE_CASE.
- Tests should be behavior-focused and human-readable.

### Error handling conventions
- Frontend API layer: fail fast with helpful error messages including status code.
- Frontend UI layer: show retry-friendly user messages when requests fail.
- Backend layer: return `404` for missing application IDs (current contract).

## Testing conventions
- Frontend tests live in `frontend/__tests__/`.
- Prefer React Testing Library queries (`screen`) and interaction helpers.
- Mock `next/navigation` in component tests when route behavior is asserted.
- Backend tests use pytest with `TestClient(app)`.
- If API contracts change, update backend models, frontend types, and tests together.

## Recommended verification before merge
```bash
./scripts/test-backend.sh
./scripts/test-frontend.sh
./scripts/test-all.sh
```
