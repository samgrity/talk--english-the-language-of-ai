# Implementation

This document explains how the prototype is structured today so new contributors can quickly map product behavior to code.

## Code Walkthrough

### Pipeline Page

**Loading the list:**
- `frontend/app/queue/page.tsx`: `QueuePage` component loads applications directly and keeps filter/search state in the URL
- `frontend/lib/api.ts`: `getApplications()` → `GET /api/applications` with filter params
- `backend/app/api/routes/applications.py`: `get_applications` endpoint
- `backend/app/services/application_service.py`: `ApplicationService.list_applications` calls repository and orders results
- `backend/app/repositories/sqlalchemy/application_repo.py`: `SqlAlchemyApplicationRepository.list_all` runs filtered SQL query
- `backend/app/services/application_service.py`: `_order_applications` sorts by status priority (waiting_for_recruiter → waiting_for_ai → waiting_for_candidate → completed)
- `frontend/components/CandidateTable.tsx`: renders the table rows

**Filtering:**
- `frontend/app/queue/page.tsx`: filter inputs (status, search) update local state
- Filter changes update URL via `router.replace` and trigger `loadApplications()` with new params
- Search input is debounced (1 second); selects fire immediately
- Same `GET /api/applications` endpoint with different query params

**Opening a candidate:**
- `frontend/components/CandidateTable.tsx`: row click calls `router.push('/review/{id}')`
- Client-side navigation only, no backend call

---

### Screening Page

**Loading the candidate:**
- `frontend/app/review/[id]/page.tsx`: `ScreenPage` instantiates `useScreenCandidate` hook
- `frontend/hooks/useScreenCandidate.ts`: `loadApplication()` on mount
- `frontend/lib/api.ts`: `getApplication(id)` → `GET /api/applications/{id}`
- `backend/app/api/routes/applications.py`: `get_application` endpoint
- `backend/app/services/application_service.py`: `ApplicationService.get_application`
- `backend/app/repositories/sqlalchemy/application_repo.py`: `SqlAlchemyApplicationRepository.get_by_id` (eager-loads company and updates)
- Hook stores both canonical and editable copies

**Editing and saving fields:**
- `frontend/components/screening/CandidateDetailsPane.tsx`: field changes call hook handlers for both candidate details and job-opening details
- `frontend/hooks/useScreenCandidate.ts`: handlers update working copy and call `markDirty()`
- Click "Update Details" → `saveApplication()` diffs canonical vs working copy
- `frontend/lib/api.ts`: `updateApplication(id, changes)` → `PUT /api/applications/{id}`
- `backend/app/api/routes/applications.py`: `update_application` endpoint
- `backend/app/services/application_service.py`: `ApplicationService.update_application`
- `backend/app/repositories/sqlalchemy/application_repo.py`: `SqlAlchemyApplicationRepository.update`
- Hook refreshes via `loadApplication()`

**Submitting a recruiter update:**
- `frontend/components/DecisionForm.tsx`: validates form, passes `NewUpdateRequest` up to hook
- `frontend/hooks/useScreenCandidate.ts`: `submitUpdate()` injects the app's default reviewer ID
- `frontend/lib/api.ts`: `addUpdate(id, request)` → `POST /api/applications/{id}/updates`
- `backend/app/api/routes/applications.py`: `add_update_to_application` endpoint
- `backend/app/services/application_service.py`: `ApplicationService.add_update` → `_add_recruiter_update`
- `backend/app/repositories/sqlalchemy/update_repo.py`: `SqlAlchemyUpdateRepository.create_for_application`
- `backend/app/services/application_service.py`: updates `screening_status`, commits via repository
- For `follow_up`: also calls outbound correspondence sender before commit
- Hook refreshes to show new update in timeline

**Triggering AI screening:**
- Submit with `update_type = "request_ai_screen"` follows same path as recruiter update
- `backend/app/services/application_service.py`: `_add_recruiter_update` sets status to `waiting_for_ai`, commits, then calls `ai_reviewer.review(app.id)` synchronously
- `AIReviewer.review()` builds the screening prompt and runs the full LLM-based screening flow defined by the `screen-candidate` skill
- AI reviewer calls back to `ApplicationService.add_update` with actor `AI_AGENT` → routes to `_add_ai_update`
- Sets status to `waiting_for_recruiter`, appends AI recommendation to updates
- Hook refresh shows AI recommendation in timeline
- External trigger: `POST /api/hooks/applications/trigger-ai-screen` fires AI directly

**Copying an AI recommendation:**
- `frontend/components/DecisionForm.tsx`: when latest update is AI recommendation, shows "Copy AI Recommendation" button
- Click → `handleCopyAIRecommendation()` maps AI update type to human equivalent (recommend_advance → advance, etc.)
- Pre-fills form fields with mapped type and correspondence
- No backend call, all data already in application state

## Frontend Structure

The frontend is a Next.js app in `frontend/` with route-level pages and reusable screening components.

### Pages

- `frontend/app/page.tsx`: client redirect to queue.
- `frontend/app/login/page.tsx`: compatibility route that redirects to the queue.
- `frontend/app/queue/page.tsx`: main pipeline listing with search/filter controls.
- `frontend/app/review/[id]/page.tsx`: two-pane screening workspace for a single candidate.

### Core Components and Hooks

- `frontend/components/CandidateTable.tsx`: pipeline table and click-through to screening pages.
- `frontend/components/screening/CandidateDetailsPane.tsx`: editable candidate details plus a separate job-opening/hiring-company section.
- `frontend/components/screening/UpdateHistoryPane.tsx`: activity timeline plus submission form area.
- `frontend/components/DecisionForm.tsx`: reviewer action form and AI action button.
- `frontend/hooks/useScreenCandidate.ts`: screening-page state orchestration.
- `frontend/lib/api.ts`: frontend API client for backend routes/hooks.
- `frontend/lib/defaultReviewer.ts`: single-reviewer defaults used by the app.

## Agent Implementation

### Skills-based approach

Instead of encoding the screening logic in code, all of it lives in a plain-English skill file (`skills/screen-candidate/SKILL.md`) with supporting reference documents. The model reads the skill, understands that it is screening a candidate against a specific job opening, and carries out the steps on its own.

### SkilledAgent

`backend/agent/skilled_agent.py` provides `SkilledAgent`, a thin subclass of `pydantic_ai.Agent` that wires up a sandboxed filesystem and skills capability.

### AIReviewer

`backend/app/services/ai_reviewer.py` is the application-level wrapper. It instantiates a `SkilledAgent` with the repository `skills/` directory, builds the screening prompt from the application data, and runs the agent. Structured output (`AIReviewOutput`) is extracted from the response and posted back to the application timeline via `ApplicationService.add_update`.

## Backend Structure

The backend is a FastAPI app in `backend/app/` organized by route, service, and repository layers.

### Routes (API layer)

- `backend/app/api/routes/applications.py`: application listing/detail/update/status/update-creation endpoints.
- `backend/app/api/routes/hooks.py`: integration hooks for external events.
- `backend/app/api/routes/recruiters.py`: recruiter list endpoint.

### Service Layer

- `backend/app/services/application_service.py` is the main orchestrator.
- `backend/app/services/ai_reviewer.py` handles AI screening via the `screen-candidate` skill and LLM tool use.
- `backend/app/services/linked_in_retriever.py` handles LinkedIn profile lookups.

### Repository Layer

- Interfaces (protocols) in `backend/app/repositories/`
- SQLAlchemy implementations in `backend/app/repositories/sqlalchemy/`
- Dependency wiring from API to service to repositories in `backend/app/api/dependencies.py`

### Data Models

- SQLAlchemy models live in `backend/app/db/models/`: `application.py`, `company.py`, `update.py`, `recruiter.py`
