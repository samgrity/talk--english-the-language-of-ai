# Correspondence Playbook

Use this file when producing `correspondence`.

## Tone requirements

- Professional, concise, helpful.
- Preserve HireFlow style used by existing templates.
- Ask only for missing information required to advance screening.

## Template mapping (`.agent/skills/screen-candidate/references/template/`)

Review these files if the scenario you are dealing with is relevant to the situations below.

- `tier_3_tier_7_info_generic.txt`
  - Use when email is personal domain (gmail/yahoo/hotmail) and you need a named company email or equivalent verification.

- `tier_3_tier_7_info_shared.txt`
  - Use when candidate used shared/role mailbox (`info@`, `admin@`, etc.).

- `website_incomplete.txt`
  - Use when website is inaccessible, incomplete, or lacks verifiable information.

- `tier_3_tier_7_upgrade_reject.txt` / `upgrade_reject_hard_no.txt`
  - Usually for decline recommendations.

- `registration_approval.txt` / `registration_approval_w_warning_language.txt`
  - Usually for advance recommendations.

## Allowed customization

You may adapt wording when needed, but keep the same basic structure and tone.

Good customization patterns:
- Replace generic ask with specific missing items.
- Remove irrelevant bullets.
- Mention exactly one or two concrete next steps.

Avoid:
- Aggressive/legal tone.
- Long questionnaires when one piece of evidence is enough.
- Requests for information already present in prior updates.

## Example: personal email + missing employment link

```
Hi {{first_name}},

Your application is being reviewed. We see you applied with a personal email address.

To continue with your screening, please share:
- A direct, named company-domain email (if available), and
- A link that confirms your current role at your company (team page or LinkedIn).

Kind regards,
The HireFlow Team
```

## Example: shared mailbox

```
Hi {{first_name}},

Your application is being reviewed. We cannot proceed under a shared or unnamed mailbox.

Please provide a direct, named company email (for example, {{first_name}}@{{org_domain}}.com), and we will continue your screening.

Best,
The HireFlow Team
```

## Example: website incomplete

```
Hi {{first_name}},

Thank you for applying.

We could not verify your company's services because the website is incomplete or inaccessible.

Please reply once your site is updated, or share an alternate professional source (LinkedIn) that confirms your company and role.

Thanks,
The HireFlow Team
```
