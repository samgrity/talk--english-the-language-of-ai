---
name: making-slides-for-john
description: Work collaboratively with John on slide decks. Start from his outline, draft slides with deck-open-slide-canvas, maintain a slide-content YAML companion file, and use hashtag comments in the YAML as the review loop.
---

# Making slides for John

This is a participatory workflow. John will guide you through the deck work. Do not treat this as a one-shot generation task.

## Core workflow

1. John writes an outline that roughly describes the slides.
2. Use the nearby `../deck-open-slide-canvas/SKILL.md` guidance to make a first draft of the deck.
3. Also create a YAML file that contains the content of every slide in a human-editable format.
4. John will then edit that YAML file and add `#` comments to draw your attention to requested changes.
5. Read those comments carefully.
6. Make the requested changes in the actual slides.
7. Update the YAML so it stays in one-to-one correspondence with the current slides.
8. Delete the corresponding `#` comments from the YAML when those requested changes are complete.

## Collaboration rules

- John is actively steering the process.
- Prefer incremental edits over large rewrites.
- Keep the YAML and the slides synchronized.
- When a requested change is ambiguous, discuss it instead of guessing.
- Do not commit unless John explicitly asks.

## Important pattern: one logical slide across several physical slides

A common pain point is when multiple slides are logically one slide.

When that happens, prefer this pattern:

- keep the **kicker** fixed
- keep the **title** fixed
- keep the text block in the **exact same position**
- keep previously introduced bullets in the **exact same position**
- reveal new bullets one at a time
- change only the **image(s) on the right side** as the sequence progresses

Critical implementation detail:

- do **not** vertically center the left text block against the right image composition when the right side changes size or complexity
- in these progressive bullet slides, top-align the main two-column layout (`items-start`, not `items-center`)
- keep the left column's top margin, title margin, and bullet-list margin identical across the whole sequence
- if needed, preserve layout stability by keeping the full bullet structure in place and only visually revealing the new bullet, rather than letting text reflow vertically
- if text still shifts, use invisible placeholders / hidden bullets to reserve space instead of allowing the list height to change the perceived position of the earlier bullets

## Deliverables

For this workflow, you will usually maintain:

- the slide deck HTML
- a slide-content YAML file
- local assets used by the deck

The YAML should be optimized for review and revision, not for visual fidelity.
