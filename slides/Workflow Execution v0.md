## Goal

Apply `Slide Workflow.md` to `Outline.md` and produce a first-pass slide planning artifact without generating slides yet.

## Step 1: Distill the talk into slide-worthy beats

Here is the current best first-pass beat map for the talk:

1. Title / thesis
2. Why this matters now
3. The old way: workflow logic in code
4. The discovery: workflows can now live in English
5. The new AI product model
6. The demo app: candidate screening
7. Start dumb: a fake review function
8. Wire in the agent
9. Show how the agent is assembled
10. Show capabilities and modularity
11. Show the LinkedIn tool as a custom extension point
12. Show where the agent gets smart: the skill file
13. Show why ordered workflow steps matter
14. Show why output structure matters
15. Show why structured internal notes matter
16. Broader pattern for building AI products
17. Gotchas
18. Follow-on idea: unharness the agent / Rook

This feels like the right order for a fast technical talk.

## Step 2: Classify each beat by slide type

| Beat | Slide type |
|---|---|
| Title / thesis | Big statement slide |
| Why this matters now | Promise / framing slide |
| The old way | Contrast slide |
| Discovery | Big statement slide |
| New AI product model | Architecture diagram slide |
| Demo app | Example / artifact slide |
| Start dumb | Process slide |
| Wire in the agent | Code-anchor slide |
| Agent assembly | Code-anchor + architecture slide |
| Capabilities and modularity | Diagram / annotated code slide |
| LinkedIn tool | Example extension slide |
| Skill file | Code-anchor slide |
| Ordered workflow steps | Process / reasoning slide |
| Output structure | Contrast / contract slide |
| Structured internal notes | Example artifact slide |
| Broader pattern | Wrap-up pattern slide |
| Gotchas | Simple list / contrast slide |
| Rook follow-on | Closing vision slide |

## Step 3: Choose one visual language

### Recommended palette

**Sea Indigo**

Why:
- dark technical keynote feel
- works well for code anchors
- strong contrast for punchy statements
- good fit for AI / systems / architecture subject matter

### Recommended style choices

- sparse text
- big typography
- one idea per slide
- minimal decorative elements
- diagrams over bullet walls
- code only when it anchors a specific point

### Things to avoid

- too many equal-weight bullets
- dense screenshots
- too much source code on screen
- generic corporate pitch-deck aesthetics

## Step 4: Draft the generation brief

Use the Open-Slide 1920 Canvas Deck template to create a fast-paced, editorial, high-contrast technical talk deck for an O'Reilly presentation titled "English is the Programming Language of AI Workflows."

Audience: technical builders who understand software, AI, and product development.

Tone: confident, sharp, slightly surprising, not corporate, not fluffy.

Use a dark Sea Indigo visual system with sparse high-impact slides. Prioritize strong headlines, architecture diagrams, process slides, and a few code-anchor slides. Avoid dense bullet lists. Each slide should have exactly one dominant visual idea.

The deck should feel like a designed conference talk, not an internal company status deck.

Use the real concepts and phrasing from `Outline.md`. Emphasize the progression from coded workflows -> English workflows -> agent harness -> skills -> broader product pattern.

Do not generate filler text, fake examples, or placeholder content.

## Step 5: First-pass slide plan

### Slide 1 — English is the Programming Language of AI Workflows
- Purpose: land the thesis immediately
- Type: big statement slide
- Speaker intent: open with the punchline, then explain why this became true recently

### Slide 2 — What changed?
- Purpose: frame why this talk matters now and not two years ago
- Type: framing slide
- Speaker intent: set up the timing argument

### Slide 3 — 2025: Workflow logic lived in code
- Purpose: contrast the old implementation-heavy way
- Type: contrast slide
- Speaker intent: remind the audience what building agent workflows used to feel like

### Slide 4 — The sinister hack
- Purpose: introduce the discovery that the workflow can now live in English
- Type: big statement slide
- Speaker intent: make the idea feel slightly illicit and exciting

### Slide 5 — The new AI product model
- Purpose: explain the architecture in one view
- Type: architecture diagram slide
- Speaker intent: explain brain / user loop / tool loop / skills

### Slide 6 — The app we’re building
- Purpose: ground the talk in a concrete product
- Type: example / artifact slide
- Speaker intent: explain the candidate-screening app and what the human used to do

### Slide 7 — Start dumb
- Purpose: show the first non-AI implementation step
- Type: process slide
- Speaker intent: explain why starting with a fake implementation lowers complexity

### Slide 8 — Where AI gets called
- Purpose: show the workflow seam in the app
- Type: code-anchor slide
- Speaker intent: point at the review entry points and hooks

### Slide 9 — The review function
- Purpose: show that the app creates a prompt and sends it to the agent
- Type: code-anchor slide
- Speaker intent: explain prompt assembly and response handling

### Slide 10 — How the agent is assembled
- Purpose: demystify the agent harness
- Type: code-anchor + architecture slide
- Speaker intent: show model, output type, capabilities, instruction

### Slide 11 — Lego blocks
- Purpose: emphasize modularity
- Type: diagram / annotated code slide
- Speaker intent: show skills, thinking, web search, web fetch as composable pieces

### Slide 12 — You can add tools
- Purpose: show custom tool extension points
- Type: example extension slide
- Speaker intent: explain the LinkedIn tool and why it exists

### Slide 13 — The skill file is where the agent gets smart
- Purpose: move smartness out of code and into English workflow definition
- Type: big statement + code-anchor slide
- Speaker intent: shift attention from Python to SKILL.md

### Slide 14 — Ordered steps matter
- Purpose: explain why the screening flow is enumerated
- Type: process / reasoning slide
- Speaker intent: connect ordered steps to steerability and debugging

### Slide 15 — Output contracts matter
- Purpose: show the value of crisp output structure
- Type: contract slide
- Speaker intent: connect `Your output` in the skill to `AIReviewOutput` in code

### Slide 16 — Internal notes are also a contract
- Purpose: show that even an internal artifact can be structured intentionally
- Type: example artifact slide
- Speaker intent: explain the checklist-shaped notes and why that helps quality

### Slide 17 — The broader pattern
- Purpose: generalize beyond this app
- Type: wrap-up pattern slide
- Speaker intent: give the reusable recipe for AI product development

### Slide 18 — Gotchas
- Purpose: show realism and balance
- Type: simple list slide
- Speaker intent: cover latency, cost, non-determinism briefly

### Slide 19 — Turn it inside out
- Purpose: end on the Rook follow-on idea
- Type: closing vision slide
- Speaker intent: move from agent-inside-app to agent-as-UX

## Step 6: Review of the plan

What feels strong:
- clear narrative arc
- good balance of concept and code
- enough concrete anchors to feel real
- finishes with a bigger product vision

What may still need adjustment:
- slide count could maybe tighten from 19 to 16–18
- the "why this matters now" section may merge with the opener
- the "Lego blocks" slide and "How the agent is assembled" slide might partially merge
- the gotchas slide should stay very short

## Step 7: Recommended next move

Before generating the deck, review this plan and make decisions on:

- final slide count target
- preferred palette
- whether to be more editorial or more code-heavy
- how much of the Rook ending to include

Once those are settled, this document can become the direct input to deck generation.

## Summary

This workflow execution produced:
- a beat map
- slide types
- a recommended visual system
- a draft generation brief
- a first-pass 19-slide plan

This is enough to critique the deck structure before generating any slides.
