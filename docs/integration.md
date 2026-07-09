# Integration

This guide covers connecting the prototype to your production systems.

## Kicking the Tires

Before wiring any production systems, you can run the AI screening agent end-to-end from the command line using the seed application files in `scripts/db/seed_data/`.

**Run a screening against seed data:**

```bash
cd backend
uv run ../scripts/review_from_seed_data.py ../scripts/db/seed_data/john_berryman.json
```

**Inspect traces:**

```bash
python scripts/navigate_traces.py -c        # count runs
python scripts/navigate_traces.py -t N      # pretty-print trace N
python scripts/navigate_traces.py -t N -f   # full detail
```

The AI screening agent's instructions and reference material live in `skills/screen-candidate/`. Editing `skills/screen-candidate/SKILL.md` or the reference files is the primary lever for improving behavior.

## Required Integrations

### 1) Trigger AI screening

- Endpoint: `POST /api/hooks/applications/trigger-ai-screen`
- Purpose: Sets the application up for processing and starts an AI screening for a specific `application_id`.
- Call this when a new application arrives or a recruiter requests a manual AI re-run.

### 2) Ingest candidate correspondence

- Endpoint: `POST /api/hooks/email/candidate-message`
- Purpose: Accepts inbound candidate messages, attaches them to the application timeline, and triggers an AI screening.
- Call this when your email layer receives a new reply from the candidate.

### 3) Send recruiter correspondence to candidate

- Method: `send_recruiter_message_to_candidate(...)` in `backend/app/integrations/email_service.py`
- Purpose: Delivers recruiter-authored candidate-facing messages through your email service.
- Implement the email API calls there.

## Data Integration Guidance

The key constraint is: **preserve the repository protocol interfaces**. These are `Protocol` classes in `backend/app/repositories/` whose method signatures are used throughout the service layer.

- `backend/app/repositories/application_repository.py`
- `backend/app/repositories/recruiter_repository.py`
- `backend/app/repositories/update_repository.py`
- `backend/app/repositories/sqlalchemy/` – current implementations
- `backend/app/db/models/` – current SQLAlchemy ORM models
- `backend/app/db/session.py` – database connection
- `backend/app/api/dependencies.py` – wires repository instances

## Enum Alignment Required

Verify and align `Department` and `SubDepartment` in both `backend/app/core/enums.py` and `frontend/types/api.ts`.

## Logging

The prototype uses Logfire for tracing. Traces are written to `logs/agent_traces.jsonl` by default. Configure a `LOGFIRE_TOKEN` environment variable for production observability.
