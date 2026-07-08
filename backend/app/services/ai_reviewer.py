"""AI screening agent.

Public surface:
  - AIReviewOutput           – structured output from the screening agent
  - AIReviewer               – SkilledAgent subclass that screens candidates
"""

import os
from calendar import month_abbr
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.capabilities import Thinking, WebFetch, WebSearch
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.anthropic import AnthropicModel, AnthropicModelSettings

from agent.skilled_agent import SkilledAgent
from app.core.config import settings
from app.core.enums import UpdateType
from app.services.linked_in_retriever import get_linkedin_profile as retrieve_linkedin_profile

_SKILLS_DIR = Path(__file__).resolve().parents[3] / "skills"
_SCREEN_CANDIDATE_SKILL = _SKILLS_DIR / "screen-candidate"
_TEMPLATES_DIR = Path(__file__).resolve().parents[3] / "templates"

_LINKDAPI_BASE = "https://linkdapi.com/api/v1/profile/full"

_SHARED_EMAIL_LOCAL_PARTS = {
    "admin",
    "contact",
    "designer",
    "hello",
    "info",
    "intern",
    "office",
    "sales",
    "support",
    "team",
}

_PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "googlemail.com",
    "yahoo.com",
    "ymail.com",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "msn.com",
    "aol.com",
    "icloud.com",
    "me.com",
    "mac.com",
}


def _load_template(template_name: str) -> str:
    """Load a plaintext correspondence template from the root templates directory."""
    template_path = _TEMPLATES_DIR / template_name
    return template_path.read_text(encoding="utf-8")


def _fill_template(template_name: str, *, first_name: str) -> str:
    """Fill template placeholders (currently only {{first_name}})."""
    template = _load_template(template_name)
    return template.replace("{{first_name}}", first_name or "there")


def _email_local_part(email: str) -> str:
    if "@" not in email:
        return ""
    return email.split("@", 1)[0].strip().lower()


def _email_domain(email: str) -> str:
    if "@" not in email:
        return ""
    return email.split("@", 1)[1].strip().lower()


def _domain_from_url(url: str) -> str:
    """Extract a normalized domain from a URL.

    Examples:
      - https://www.example.com/about -> example.com
      - example.com -> example.com
    """
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = (parsed.netloc or parsed.path).strip().lower()
    return host[4:] if host.startswith("www.") else host


def _format_prior_updates_for_prompt(application: Any, max_items: int = 25) -> str:
    """Render recent prior updates for agent context.

    This ensures the screening skill can explicitly see whether a judgment came from
    a human recruiter or AI agent (via ``actor``), and can apply the rule that
    human judgments supersede AI judgments.
    """
    if not application.updates:
        return "None"

    # Enforce chronological ordering so later updates are last.
    updates_in_order = sorted(application.updates, key=lambda u: u.timestamp)
    recent = updates_in_order[-max_items:]

    docs: list[str] = []
    for idx, update in enumerate(recent, start=1):
        notes = (update.internal_notes or "").strip()
        correspondence = (update.correspondence or "").strip()
        actor = getattr(update.actor, "value", str(update.actor))
        update_type = getattr(update.update_type, "value", str(update.update_type))
        recruiter_id = update.recruiter_id or "null"

        doc = (
            "---\n"
            f"index: {idx}\n"
            f"timestamp: {update.timestamp.isoformat()}\n"
            f"actor: {actor}\n"
            f"update_type: {update_type}\n"
            f"recruiter_id: {recruiter_id}\n"
            "---\n\n"
            "### internal_notes\n"
            f"{notes or '(none)'}\n\n"
            "### correspondence\n"
            f"{correspondence or '(none)'}\n"
        )
        docs.append(doc)

    return "\n\n".join(docs)


async def _try_algorithmic_handling(application_id: str, application: Any, service: Any) -> bool:
    """Try deterministic handling before full agentic/manual screening.

    Returns:
      - True: this function already called ``service.add_update(...)`` and the
        caller should return early.
      - False: nothing deterministic matched; continue into manual/agentic screening.


    IMPORTANT CONSTRAINTS (intentional for current phase):

    Uses only data already present on ``application`` and ``application.company``.
    If we need richer automation, we should extend the data model later.


    Automatic rules implemented now:
      1) Company already flagged -> recommend_decline.
      2) Junior candidate without .edu email -> recommend_decline.
      3) Shared mailbox email (info@, admin@, etc.) -> recommend_follow_up.
      4) Public mailbox domain (gmail/yahoo/etc.) -> recommend_follow_up.
      5) Company verified + email domain matches company site domain
         -> recommend_advance.

    Future work (requires richer model data, intentionally deferred):
      - Domain trust / prior-advanced-count checks for true auto-advance.
      - Strong company-level auto-decline propagation policy with explicit flags.
      - More precise junior candidate flow messaging templates.
      - Explicit fields for "sole proprietor" and "email seen on company site" to
        avoid conservative follow-up outcomes for shared/public emails.
      - Additional deterministic paths (brand reps, duplicates, known bad actors).
    """
    from app.core.enums import CompanyVerificationStatus, UpdateActor

    first_name = application.firstName
    email = (application.email or "").strip()
    local_part = _email_local_part(email)
    domain = _email_domain(email)
    seniority = (application.seniorityLevel or "").strip().lower()
    company = application.company
    company_domain = _domain_from_url(company.siteUrl or "")

    if company.verificationStatus == CompanyVerificationStatus.FLAGGED:
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.RECOMMEND_DECLINE,
            internal_notes=(
                "Algorithmic handling: company is already flagged. "
                "Recommend declining this application to align with current "
                "company-level decision."
            ),
            correspondence=_fill_template("upgrade_reject_hard_no.txt", first_name=first_name),
            recruiter_id=None,
        )
        return True

    if "junior" in seniority and not domain.endswith(".edu"):
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.RECOMMEND_DECLINE,
            internal_notes=(
                "Algorithmic handling: candidate is marked as junior but "
                "email domain is not .edu. Recommend declining under current "
                "deterministic junior candidate rule."
            ),
            correspondence=_fill_template("upgrade_reject_hard_no.txt", first_name=first_name),
            recruiter_id=None,
        )
        return True

    if local_part in _SHARED_EMAIL_LOCAL_PARTS:
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.RECOMMEND_FOLLOW_UP,
            internal_notes=(
                "Algorithmic handling: shared/role mailbox detected from email local "
                f"part '{local_part}'. Recommend requesting a direct, named email "
                "before proceeding."
            ),
            correspondence=_fill_template("tier_3_tier_7_info_shared.txt", first_name=first_name),
            recruiter_id=None,
        )
        return True

    if domain in _PUBLIC_EMAIL_DOMAINS:
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.RECOMMEND_FOLLOW_UP,
            internal_notes=(
                "Algorithmic handling: personal email domain detected. Recommend asking "
                "for named company-domain email (or additional verification) before "
                "proceeding."
            ),
            correspondence=_fill_template("tier_3_tier_7_info_generic.txt", first_name=first_name),
            recruiter_id=None,
        )
        return True

    if company.verificationStatus == CompanyVerificationStatus.VERIFIED and company_domain and domain == company_domain:
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.RECOMMEND_ADVANCE,
            internal_notes=(
                "Algorithmic handling: company is already verified and candidate "
                "email domain matches company site domain. Recommend advancing."
            ),
            correspondence=_fill_template("registration_approval.txt", first_name=first_name),
            recruiter_id=None,
        )
        return True

    return False


# ---------------------------------------------------------------------------
# AIReviewOutput
# ---------------------------------------------------------------------------

class AIReviewOutput(BaseModel):
    """Structured output produced by the AI screening agent for each candidate."""
    update_type: UpdateType
    internal_notes: str
    correspondence: str | None = None

# ---------------------------------------------------------------------------
# AIReviewer
# ---------------------------------------------------------------------------

class AIReviewer(SkilledAgent):
    """Singleton AI screening agent. Constructed once at module load; service is
    passed per-call so the agent can be shared across requests."""

    def __init__(self) -> None:
        super().__init__(
            model=AnthropicModel(
                'claude-sonnet-5',
                settings=AnthropicModelSettings(anthropic_thinking={'type': 'adaptive'}),
            ),
            skills=[_SCREEN_CANDIDATE_SKILL],
            output_type=AIReviewOutput,
            capabilities=[Thinking(effort='high'), WebSearch(), WebFetch()],
        )

        @self.tool
        async def get_linkedin_profile(
            ctx: RunContext[None],
            first_name: str,
            last_name: str,
            company_name: str | None = None,
            company_url: str | None = None,
            linked_in_username: str | None = None,
        ) -> str:
            """Look up the LinkedIn profile for a candidate.

            Performs a web search to find their LinkedIn username, then fetches
            and returns their full profile as Markdown. Returns an 'ERROR:'
            string if the lookup fails at any stage, describing what was
            attempted and why it failed.
            """
            return await retrieve_linkedin_profile(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                company_url=company_url,
                linked_in_username=linked_in_username,
                message_history=list(ctx.messages),
            )

    async def review(self, application_id: str, service: Any) -> None:
        from app.core.enums import UpdateActor

        application = await service.get_application(application_id)

        has_been_handled = await _try_algorithmic_handling(
            application_id=application_id,
            application=application,
            service=service,
        )
        if has_been_handled:
            return

        company_verification_status = getattr(
            application.company.verificationStatus,
            "value",
            str(application.company.verificationStatus),
        )
        company_scope_guidance = (
            " (Company already verified: do NOT spend time re-investigating the company.)"
            if company_verification_status == "verified"
            else ""
        )

        prompt = (
            f"Application ID: {application_id}\n"
            f"Candidate: first_name=\"{application.firstName}\", last_name=\"{application.lastName}\"\n"
            f"Email: {application.email}\n"
            f"Job title: {application.jobTitle}\n"
            f"Seniority level: {application.seniorityLevel}\n"
            f"Company: {application.company.name}\n"
            f"Company site: {application.company.siteUrl}\n"
            f"Company type: {application.company.type}\n"
            f"Company verification status: {company_verification_status}{company_scope_guidance}\n"
            f"LinkedIn URL: {application.linkedinUrl}\n"
            f"Department: {application.department}\n"
            f"Region: {application.region}\n"
            "\nPrior updates (chronological; later updates are last; each entry is markdown with YAML frontmatter):\n"
            f"{_format_prior_updates_for_prompt(application)}\n"
            "\nPlease screen this candidate using the screen_candidate skill."
        )
        result = await self.run(prompt)
        output: AIReviewOutput = result.output
        await service.add_update(
            application_id=application_id,
            actor=UpdateActor.AI_AGENT,
            update_type=output.update_type,
            internal_notes=output.internal_notes,
            correspondence=output.correspondence,
            recruiter_id=None,
        )
