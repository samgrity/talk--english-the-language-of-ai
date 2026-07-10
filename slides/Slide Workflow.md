# Slide Workflow

## Goal

Turn `Outline.md` into a strong slide deck without generating the deck too early.

## Overall approach

1. Distill the talk into slide-worthy beats.
2. Classify each beat by slide type.
3. Pick one visual language for the whole deck.
4. Write a generation brief for the deck skill.
5. Review the proposed slide plan before generating slides.
6. Generate the first draft deck.
7. Tighten and simplify.

## Step 1: Distill the talk into slide-worthy beats

The outline is not the same thing as a slide deck.

First, compress the talk into a smaller set of presentation beats, probably something like 12–18 slides total.

Likely beats for this talk:

- Title / promise
- The old way: workflow logic buried in code
- The discovery: English can now express the workflow
- The new architecture: model + tools + skills + shim
- The demo app: candidate review workflow
- Start dumb: canned review function
- Add the agent harness
- Add capabilities and tools
- Make the agent smart in the skill file
- Ordered workflow steps matter
- Output schema matters
- Structured internal notes matter
- Iterate, evaluate, improve
- Broader applicability
- Rook / unharnessing the agent

## Step 2: Classify each beat by slide type

Each beat should become a specific kind of slide.

Useful slide types for this talk:

- Big statement slide
- Contrast slide
- Architecture diagram slide
- Code-anchor slide
- Process slide
- Example / artifact slide
- Wrap-up slide

Examples:

- "English is the programming language of AI workflows" -> big statement slide
- "2025 vs 2026" -> contrast slide
- "Brain / user loop / tool loop / skills" -> architecture diagram slide
- `ai_reviewer.py` or `SKILL.md` -> code-anchor slide
- "dumb function -> agent -> skill-driven workflow" -> process slide

Rule of thumb: one dominant idea per slide.

## Step 3: Pick one visual language

Choose the deck style once and keep it fixed.

For this deck, likely good options are:

- **Sea Indigo**: dark, technical, keynote-like
- **Ash & Lime**: modern, slightly strange, energetic
- **Pearl Rose**: more editorial and distinctive

Also decide:

- sparse vs dense text
- technical vs editorial tone
- how often code appears
- whether diagrams should be abstract or literal

Recommendation: sparse, high-contrast, technical-editorial, with very little dense text.

## Step 4: Write the generation brief

Do not just say "make slides from this outline."

The brief should specify:

- audience
- tone
- slide count target
- preferred slide types
- visual language
- pace
- what to emphasize
- what to avoid

For this talk, the brief should probably say:

- fast-paced O'Reilly talk
- technical audience
- not corporate
- not overloaded with bullets
- emphasize big ideas, architecture, and a few code anchors
- keep slides easy to talk over
- prefer strong headlines and sparse layouts
- use the actual language from `Outline.md`

## Step 5: Review the slide plan before generation

Before generating any deck, create a slide-by-slide plan.

For each slide, define:

- slide number
- working title
- purpose
- slide type
- source section from `Outline.md`
- short speaker-note intent

This is the quality checkpoint.

If the slide plan is good, the generated deck will usually be much better.

## Step 6: Generate the first draft deck

Use the deck skill only after the plan is solid.

Generation input should include:

- the slide plan
- the outline
- the chosen palette / visual language
- explicit instruction to keep one visual focal point per slide
- instruction to minimize filler and dense bullet walls

## Step 7: Tighten and simplify

After generation, review for:

- too much text
- repeated ideas
- slides with more than one focal point
- code slides that are too hard to read
- weak transitions between sections
- ending that does not land clearly

Typical cleanup moves:

- split overloaded slides
- merge repetitive slides
- replace bullets with one strong sentence
- turn some explanation slides into diagrams
- sharpen the ending and the "why this matters" section

## Practical recommendation for this talk

Before generating slides, the next best move is to create a dedicated slide plan note in this folder.

Suggested next file:

- `Slide Plan.md`

That file should map the talk into an actual sequence of slides, but still stop short of generating the deck.

## Output of this workflow

If done well, this folder should eventually contain:

- `Outline.md`
- `Slide Workflow.md`
- `Slide Plan.md`
- generated deck assets later

## Summary

The workflow is:

1. Outline the talk.
2. Distill it into beats.
3. Turn beats into slide types.
4. Choose one visual system.
5. Write a strong generation brief.
6. Build and review a slide plan.
7. Only then generate the deck.
8. Tighten the result.
