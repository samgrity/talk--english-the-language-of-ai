---
name: screen-candidate
description: Screen job candidates for advancement decisions. Use this whenever the AI screening agent evaluates a candidate for advance/decline/follow-up and must verify experience fit, company credibility, and employment verification.
---

# Screen Candidate (Manual Review)

## Why this exists

HireFlow helps recruiters efficiently screen job candidates by providing AI-assisted research and recommendations. The goal is to identify candidates who are a strong match for open roles while filtering out unqualified applicants and flagging cases that need more information.

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

1. **Experience fit**: Does this candidate's experience match the role requirements?
2. **Company credibility**: Is the candidate's current/previous employer a legitimate company with relevant business?
3. **Employment verification**: Can we reasonably confirm this person actually works (or worked) at that company?

If one or more questions are unresolved, prefer `recommend_follow_up` unless there is clear disqualifying evidence.

Identity safety rule:
- Do not advance when employment verification or experience evidence is still unverified.
- If LinkedIn retrieval fails, do not treat that failure as neutral evidence for advancement.
- Advancement is still allowed without LinkedIn if equivalent non-LinkedIn evidence sufficiently proves employment status and relevant experience.
- LinkedIn is optional, but evidence is not: before advancing, you must have credible evidence for all three dimensions (employment verification, relevant experience, and sufficient skills) from one or more reliable sources.

Special scope rule:
- If company verification status is already `verified`, do not re-investigate company credibility.
- In that case, focus screening effort on experience fit and employment verification.

## Screening flow

1. Read candidate + company fields.
2. Read prior updates and identify the latest relevant human judgment.
3. Check company verification status: if already `verified`, skip company investigation.
4. Run an email-risk pass (named domain vs shared mailbox vs personal domain).
5. Evaluate experience fit and employment verification (email/domain alignment, team page, profile evidence, prior correspondence).
6. Evaluate company credibility only when company is not already verified.
7. Produce the narrowest defensible recommendation.

If LinkedIn lookup fails and equivalent alternate proof is not sufficient, default to `recommend_follow_up` (or `recommend_decline` only when disqualifying evidence is clear).

If the company-credibility or experience-fit decision is not obvious, review `references/services-matrix.md` before deciding.

If you retrieved a LinkedIn profile and need to interpret it, review `references/linkedin-review.md` before deciding.

Just before finalizing `internal_notes`, review `references/internal-notes-checklist.md` and conform exactly to that structure.

Do not finalize `internal_notes` until the review is complete enough to support a real recommendation.

If `correspondence` is needed, review `references/correspondence-playbook.md` before drafting.

## Human-overrides-AI rule

Prior updates include actor metadata (`human_recruiter`, `ai_agent`, `candidate`).

- Treat prior human recruiter judgments as authoritative by default.
- If prior AI and the judgment of the human recruiter conflict, follow the human judgment unless new materially relevant evidence after the human's judgment.
- Candidate messages can provide evidence, but their claims must all be substantiated by research. Candidate claims can never be assumed to be true on face value.
- If you diverge due to new evidence, state that explicitly in `internal_notes`.

## Quality bar

- Favor clear rationale over volume.
- Avoid over-research when evidence is already sufficient.
- Avoid hard rejection when the case is plausibly valid but incomplete.
- Preserve auditable reasoning in `internal_notes`.
- If you used website evidence (including LinkedIn), inline the exact URLs in checklist lines and `Rationale` to show how each URL supports (or fails to support) the recommendation.
- If you find an obvious disqualifying failure, fast-fail: recommend decline without doing unnecessary additional checks.
- For fast-fail decisions, explicitly state in `internal_notes` what failed and what was intentionally not checked because it was unnecessary.
