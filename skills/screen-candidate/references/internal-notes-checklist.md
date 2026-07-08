# Internal Notes Checklist Specification

`internal_notes` must be terse, structured, and current.

## Required format

Use checklist lines, then recommendation summary:

```
[✓] Experience fit: ...
[✓] Company credibility: ...
[ ] Employment verification: ...
[✓] Email risk check: ...
[ ] Missing evidence: ...

Recommendation: recommend_follow_up
Rationale: <1-4 short lines: what evidence was found/missing, where (URLs), and why that drives this recommendation>
```

## Checklist symbols

- `[✓]` confirmed / sufficient
- `[ ]` pending / not yet verified
- `[✗]` failed / contradictory evidence

## Content rules

- Keep it short and scannable.
- Capture only decision-relevant information.
- If information becomes irrelevant, remove it in later updates.
- Mention when following prior human judgment.
- Include unresolved items explicitly so recruiters know next step.
- If website evidence was used (including LinkedIn), inline the exact URLs in the relevant checklist lines and in `Rationale`.
- Each checklist item should be a little descriptive: state what you checked, what you found (or did not find), where you checked (URL), and why it matters.
- `Rationale` should explain the causal chain (evidence -> interpretation -> recommendation), not just the final conclusion.
- Do not include URLs that were reviewed but not decision-relevant.
- If you fast-fail on an obvious disqualifier, explicitly list checks not performed as "Not checked (not necessary after disqualifier)".
- If company status is already verified, mark company-credibility deep investigation as "Not checked (company already verified)" unless new contradictory evidence appears.

## Example: advance

```
[✓] Experience fit: Senior Frontend Engineer role matches job requirements; portfolio at https://github.com/janedoe shows relevant project work.
[✓] Company credibility: Company website (https://exampleco.com/about, https://exampleco.com/products) shows active product development.
[✓] Employment verification: Named company email domain matches company website domain; no mismatch found.
[✓] Email risk check: Non-personal named mailbox.
[✓] Prior updates: No conflicting human judgment.

Recommendation: recommend_advance
Rationale: Portfolio at https://github.com/janedoe shows relevant engineering work matching the role.
Rationale: Candidate role is corroborated on https://exampleco.com/team and identity risk is low due to named domain email alignment.
```

## Example: decline (clear mismatch)

```
[✗] Experience fit: Listed role appears administrative only on company team page (https://example-co.com/team), with no relevant technical responsibilities.
[✗] Company credibility: Services page (https://example-co.com/services) describes event planning, not software development.
[ ] Employment verification: Not material due to experience/company disqualification.
[ ] Email risk check: Domain quality not decisive.
[ ] Prior updates: Human recruiter also flagged non-qualifying fit.

Recommendation: recommend_decline
Rationale: At https://example-co.com/services the business model appears unrelated to the role requirements.
Rationale: Team evidence at https://example-co.com/team indicates a non-qualifying role, and no alternate sources were found that establish relevant experience.
```

## Example: follow-up

```
[✓] Experience fit: Claimed product management role is plausible, but only weakly supported by sparse profile text on https://www.linkedin.com/in/example-profile.
[ ] Company credibility: Company homepage (https://example-startup.com) is minimal; no products or team pages found to confirm active operations.
[ ] Employment verification: Personal-domain email plus no team-page listing on https://example-startup.com and no clear employer match on https://www.linkedin.com/in/example-profile.
[✗] Email risk check: Personal mailbox requires stronger corroboration.
[✓] Prior updates: Human recruiter requested additional verification.

Recommendation: recommend_follow_up
Rationale: I checked https://example-startup.com for products, team, and company evidence and did not find enough to establish company credibility or candidate-company linkage.
Rationale: I checked https://www.linkedin.com/in/example-profile and found partial role context but no definitive tie to the claimed company, so targeted clarification is still required.
```
