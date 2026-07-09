---
name: screen-candidate
description: Screen job candidates for advancement decisions. Use this whenever the AI screening agent evaluates a candidate for advance/decline/follow-up and must judge fit against a specific job opening using the candidate profile, job-opening details, prior updates, and external evidence.
---

# Screen Candidate (Manual Review)

## Why this exists

HireFlow helps reviewers screen candidates for a clearly defined job opening. The goal is to identify candidates who are a strong fit for the posted role while avoiding overconfident decisions when the evidence is thin.

Your job is to recommend whether a candidate should be advanced, declined, or followed up with for more information.

This skill handles the full screening workflow from research through recommendation.

## Your output

Your final output must contain exactly these fields:
- `update_type`: `recommend_advance` | `recommend_decline` | `recommend_follow_up`
- `internal_notes`: required and must conform to `references/internal-notes-checklist.md`
- `correspondence`: required for `recommend_follow_up`; optional otherwise

Important:
- Do not emit the final output structure early.
- Do not emit placeholder, partial, progress-update, or empty values in the final output structure.
- Do not return the final output structure immediately after loading this skill.
- Return the final output structure only after you have completed the required research, applied the screening flow, and made a real recommendation decision based on the instructions in this skill.
- If research is still in progress, continue using tools and thinking; do not produce the final structured output yet.

## Decision model

Always answer these three questions in order:

1. **Role fit**: Does the candidate's demonstrated background match the posted job opening, including the title, department, seniority, and job description?
2. **Evidence quality**: Do we have enough credible public/profile evidence to support that fit judgment?
3. **Follow-up need**: Is there a narrow missing piece that could materially change the decision?

If role fit is clearly weak, prefer `recommend_decline`.
If role fit looks plausible but evidence is incomplete or ambiguous, prefer `recommend_follow_up`.
Advance only when the candidate appears to be a strong fit and the evidence is sufficient.

Identity safety rule:
- Do not advance when relevant experience or role-fit evidence is still too weak to justify confidence.
- If LinkedIn retrieval fails, do not treat that failure as neutral evidence for advancement.
- LinkedIn is optional, but credible evidence is not.
- Advancement can be supported by LinkedIn, personal/company websites, portfolios, talks, GitHub, prior updates, or other reliable public evidence.

## Screening flow

1. Read candidate details and the full job opening details.
2. Read prior updates and identify the latest relevant human judgment.
3. Read the job description carefully before deciding whether the profile matches.
4. Run a quick email-risk pass (named domain vs shared mailbox vs personal domain) only as supporting context.
5. Evaluate role fit using public evidence, prior updates, and the candidate's materials.
6. If fit is unclear, gather the minimum additional evidence needed.
7. Produce the narrowest defensible recommendation.

If the fit decision is not obvious, review `references/services-matrix.md` before deciding.

If you retrieved a LinkedIn profile and need to interpret it, review `references/linkedin-review.md` before deciding.

Just before finalizing `internal_notes`, review `references/internal-notes-checklist.md` and conform exactly to that structure.

Do not finalize `internal_notes` until the review is complete enough to support a real recommendation.

If `correspondence` is needed, review `references/correspondence-playbook.md` before drafting.

## Human-overrides-AI rule

Prior updates include actor metadata (`human_recruiter`, `ai_agent`, `candidate`).

- Treat prior human reviewer judgments as authoritative by default.
- If prior AI and the judgment of the human reviewer conflict, follow the human judgment unless there is new materially relevant evidence after the human judgment.
- Candidate messages can provide useful context, but their claims still need supporting evidence when the claim matters to the decision.
- If you diverge due to new evidence, state that explicitly in `internal_notes`.

## Quality bar

- Favor clear rationale over volume.
- Avoid over-research when evidence is already sufficient.
- Avoid hard rejection when the case is plausibly valid but incomplete.
- Preserve auditable reasoning in `internal_notes`.
- If you used website evidence (including LinkedIn), inline the exact URLs in checklist lines and `Rationale` to show how each URL supports (or fails to support) the recommendation.
- If you find an obvious disqualifying mismatch, fast-fail: recommend decline without doing unnecessary additional checks.
- For fast-fail decisions, explicitly state in `internal_notes` what failed and what was intentionally not checked because it was unnecessary.
