# Demo Guide

## 1. Documentation overview

Walk through the docs folder and README briefly.

- `README.md` – what the system is, walk-through, quick start
- `docs/implementation.md` – how the prototype is built: UI pages, backend layers, agent harness, skills-based approach
- `docs/integration.md` – how to wire it to production: inbound hooks, DB layer, email outbound, logging
- `docs/future_work.md` – path from recommendation-only to automated action: logging, recruiter feedback, coding analysis, skill iteration

## 2. UI walkthrough

- **Pipeline**
  - default view (pending candidates)
  - filter by status and free-text search
  - status priority ordering (waiting for recruiter → AI → candidate → completed)
- **Screening workspace**
  - left pane: separate candidate-details and job-opening sections, including hiring company and job description
  - right pane: activity timeline (AI recommendations, recruiter decisions, candidate correspondence)
  - submission form: action types, correspondence draft
  - "Copy AI Recommendation" button – pre-fills form from latest AI recommendation
  - trigger AI screening manually from the form

## 3. Live AI screening demos

### Jane Doe (ExampleCo) – LinkedIn mismatch case
- Good-looking application on the surface: legit company, plausible role
- Trigger AI screening and walk through the recommendation
- Point out where LinkedIn doesn't match expected work type – AI should catch this
- Show the internal notes and draft correspondence the AI produces

### Re-screen with additional context
- Simulate a case where the human reviewer has gathered extra info
- Add that context as a human update in the timeline
- Trigger AI screening again and show how the recommendation changes with the richer context

## 4. Command-line seed data demo

Good way to kick the tires before wiring anything.

```bash
cd backend
uv run ../scripts/review_from_seed_data.py ../scripts/db/seed_data/john_berryman.json
```

- Runs the full AI screening agent against seed JSON, no DB or hooks needed
- Prints structured `AIReviewOutput` JSON
- Traces logged to `logs/agent_traces.jsonl`

Inspect traces:
```bash
python scripts/navigate_traces.py -c        # count runs
python scripts/navigate_traces.py -t N      # pretty-print trace N
python scripts/navigate_traces.py -t N -f   # full detail
```

## 5. Integration walkthrough (engineers)

Walk through `docs/integration.md`:

- Inbound hooks: new application → `trigger-ai-screen`; email reply → `candidate-message`
- Outbound: `send_recruiter_message_to_candidate` stub
- DB layer: preserve repository interfaces, replace/adapt SQLAlchemy implementations
- Screening behavior is driven by the `screen-candidate` skill and supporting references
- Enum alignment: `Department` and `SubDepartment`
- Logfire token → full observability in production

## 6. Future work discussion

Walk through `docs/future_work.md`:

- Improve AI screening accuracy as a goal in itself (saves recruiter time)
- Logging + adoption tracking as the foundation
- Recruiter annotation UI, open/axial coding to categorize tasks
- Iterating on skills files to fix weaknesses
- Path to automation: high-accuracy + low-risk tasks → AI takes real actions
- Brainstorm: other tasks or workflows this approach could apply to
