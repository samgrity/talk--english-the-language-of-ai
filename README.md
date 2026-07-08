# HireFlow Candidate Screening System

This repository is a working prototype for AI-assisted candidate screening.

At a high level, recruiters move through a pipeline of applications, open an individual screening workspace, and record decisions with optional candidate correspondence. The AI assists them by proactively performing research based on the process described in the skills directory. The AI then provides recommended next steps including notes to justify their decision and draft correspondence.

In the future if the AI agent tends to make good decisions then their recommendations can be turned into actual actions taken to advance or decline candidates or to request more information.

## Documentation

- [Implementation](docs/implementation.md) – How the prototype is structured: frontend pages and components, backend routes/services/repositories, data models, and the end-to-end screening workflow.
- [Integration](docs/integration.md) – How to connect the prototype to production systems: inbound/outbound hook endpoints, data/database integration guidance, enum alignment, and AI provider wiring.
- [Future Work](docs/future_work.md) – Path toward improving AI screening quality and automating low-risk tasks: logging, recruiter feedback workflows, skill iteration, and full automation.

## Walk Through

A recruiter starts by selecting their identity from the login screen – a lightweight placeholder until real authentication is in place.

From there they land in the candidate pipeline, which shows every pending application assigned to them by default. The pipeline can be filtered by screening status, assignee, or a free-text search across any field, making it easy to triage across all candidates or focus on a specific slice of work.

Opening a candidate brings up a two-pane workspace. The left side shows editable candidate and company details – the recruiter can correct or enrich any field and save changes at any time. The right side shows the full activity timeline: a chronological view of AI recommendations, recruiter decisions, and candidate correspondence all in one place. At the bottom of the right pane, the recruiter can submit a new update – choosing an action such as advancing, declining, requesting more information, or triggering a fresh AI screening.

When the AI has run, its recommendation appears as an entry in the activity timeline with internal notes and a draft candidate-facing message. If the recruiter agrees, they can copy that recommendation directly into the submission form rather than writing from scratch.

The AI can be triggered automatically when a new application arrives or when a candidate replies, keeping the pipeline moving without requiring manual intervention. Recruiter decisions are recorded as part of the same activity timeline, so the full story of each candidate – what the AI found, what the candidate said, and what the recruiter decided – is always visible in one place.

## High-Level Structure

- `frontend/`: recruiter-facing application.
- `backend/`: API server, business logic, and persistence layer.
- `scripts/`: operational helpers for startup, testing, and DB reset.
- `docs/`: implementation, integration, and future work guidance.

## Scripts Guide (`scripts/`)

Use these scripts for consistent local dev/test workflows.

| Script | What it does | When to use it |
|---|---|---|
| `scripts/start-all.sh` | Installs deps if needed, restarts any services already on ports 8000/3000, then runs backend and frontend together until stopped | Daily local development and clean restarts |
| `scripts/test-backend.sh` | Runs backend pytest suite via `uv` | Validating backend changes |
| `scripts/test-frontend.sh` | Runs frontend Jest coverage + `tsc --noEmit` + Next build | Validating frontend changes |
| `scripts/test-all.sh` | Runs backend and frontend test scripts with summary output | Pre-merge confidence check |
| `scripts/reinitialize_db.sh` | Rebuilds and reseeds prototype DB state | Resetting local data for repeatable testing |
| `scripts/navigate_traces.py -c` | Count model-traffic traces in `logs/agent_traces.jsonl` | Quick check of how many AI screening runs have been logged |
| `scripts/navigate_traces.py -t N [-f]` | Pretty-print trace N with colour-coded messages, thinking, tool calls, and responses | Debugging AI screening runs |
| `scripts/retrieve_linked_in.py <seed_file>` | Loads a seed JSON, resolves LinkedIn username/profile via the retriever service | Debugging LinkedIn resolution |
| `scripts/review_from_seed_data.py <seed_file>` | Loads a seed JSON, runs `AIReviewer` with the same prompt shape used in service flow | Manually validating AI behavior from seed data |

## Quick Start

From repository root:

```bash
./scripts/start-all.sh
```

Local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
