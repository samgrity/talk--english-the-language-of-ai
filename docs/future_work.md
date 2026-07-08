# Future Work

The prototype saves recruiter time by doing research and drafting correspondence, but the AI screening agent only recommends next steps – it does not act. This document describes two related goals: improving accuracy of AI screenings and identifying tasks the AI handles reliably enough to automate.

## Setup: Logging

Logging is the prerequisite for everything else. Before doing any analysis, make sure every AI screening run is fully traced and that the data captures whether the recruiter adopted the AI's recommendation or discarded it in favour of a different action.

## Evaluating AI Screenings

Start with the logs. Look at adoption patterns – how often recruiters use the AI's recommendation as-is versus how often they override it.

## Extending the UI for Recruiter Feedback

Raw adoption data only tells you that something went wrong, not what or why. Add lightweight UI controls so recruiters can annotate AI interactions directly: flagging poor recommendations, noting what the correct action should have been, and rating the quality of draft correspondence.

When enough annotations have been collected, analyze them using an open coding / axial coding approach. Open coding means reading through the interactions without preconceptions and labeling what the AI is actually trying to do in each case. Axial coding then groups those labels into clusters and surfaces relationships between them.

## Identifying and Documenting Weaknesses

For every case where the AI erred – recommended the wrong action, missed a red flag, drafted inappropriate correspondence – document specifically what went wrong and what the correct behavior should have been.

## Improving the Skills

The AI screening agent's behavior is governed by the instructions and reference material in `skills/screen-candidate/`. These files are plain English, and the AI treats them the way a new human recruiter would treat their onboarding documentation.

Use the weakness documentation to drive iterative edits. Changes should be validated against the seed data scripts before deploying to production.

## Tracking Success Rates by Task

As more annotation data accumulates, start tracking success rates broken down by task category. This makes it possible to measure improvement over time and identify which categories have reached sufficient accuracy to consider automation.

## Automating Low-Risk Tasks

When a task category has both high accuracy and low risk – meaning the AI gets it right consistently and a wrong answer has limited consequences – it becomes a candidate for full automation. At that point, the AI does not just recommend but actually takes action: advancing or declining obvious cases outright, and sending follow-up messages directly to candidates.
