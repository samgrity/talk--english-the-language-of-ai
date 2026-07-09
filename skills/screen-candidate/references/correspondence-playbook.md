# Correspondence Playbook

Use this file when producing `correspondence`.

## Tone requirements

- Professional, concise, helpful.
- Preserve HireFlow style used by existing templates.
- Ask only for missing information required to advance screening.

## Template mapping (`.agent/skills/screen-candidate/references/template/`)

Review these files if the scenario you are dealing with is relevant to the situations below.

- `tier_3_tier_7_info_generic.txt`
  - Use when you need one or two concrete public/professional artifacts to confirm role fit, including the correct LinkedIn profile when it could not be retrieved.

- `tier_3_tier_7_info_shared.txt`
  - Use when candidate used shared/role mailbox (`info@`, `admin@`, etc.).

- `website_incomplete.txt`
  - Use when the candidate's public materials are too thin to confirm fit.

- `tier_3_tier_7_upgrade_reject.txt` / `upgrade_reject_hard_no.txt`
  - Usually for decline recommendations.

- `registration_approval.txt` / `registration_approval_w_warning_language.txt`
  - Usually for advance recommendations.

## Allowed customization

You may adapt wording when needed, but keep the same basic structure and tone.

Good customization patterns:
- Replace a generic ask with specific missing items.
- Remove irrelevant bullets.
- Mention exactly one or two concrete next steps.

Avoid:
- Aggressive/legal tone.
- Long questionnaires when one piece of evidence is enough.
- Requests for information already present in prior updates.

## Example: missing LinkedIn profile + insufficient evidence

```
Hi {{first_name}},

Thanks for your application.

To continue the screening for this role, please reply with:
- your correct LinkedIn profile URL, and
- one or two concrete examples of closely related work, such as a portfolio / GitHub / case-study link or a short description of a recent project that best matches this opening.

Best,
The HireFlow Team
```

## Example: shared mailbox

```
Hi {{first_name}},

Your application is being reviewed. We cannot proceed under a shared or unnamed mailbox.

Please provide a direct, named professional email address and we will continue your screening.

Best,
The HireFlow Team
```

## Example: public materials too thin

```
Hi {{first_name}},

Thank you for applying.

We were not able to find enough public detail to evaluate your fit for this role.

Please reply with your correct LinkedIn profile URL and one or two relevant links or examples that best represent your experience for this opening.

Thanks,
The HireFlow Team
```
