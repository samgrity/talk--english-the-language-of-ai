"""AI screening agent.

Public surface:
  - AIReviewOutput           – structured output from the screening agent
  - AIReviewer               – SkilledAgent subclass that screens candidates
"""

from calendar import month_abbr
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_ai import RunContext
from pydantic_ai.capabilities import Thinking, WebFetch, WebSearch
from pydantic_ai.models.anthropic import AnthropicModel, AnthropicModelSettings

from agent.skilled_agent import SkilledAgent
from app.core.enums import UpdateType
from app.services.linked_in_retriever import get_linkedin_profile as retrieve_linkedin_profile

_SKILLS_DIR = Path(__file__).resolve().parents[3] / "skills"
_SCREEN_CANDIDATE_SKILL = _SKILLS_DIR / "screen-candidate"


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


# ---------------------------------------------------------------------------
# AIReviewOutput
# ---------------------------------------------------------------------------

class AIReviewOutput(BaseModel):
    """Structured output produced by the AI screening agent for each candidate."""
    update_type: UpdateType
    internal_notes: str = Field(min_length=1)
    correspondence: str | None = None

    @field_validator("internal_notes")
    @classmethod
    def internal_notes_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("internal_notes must be a non-empty string")
        return value

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

        job_opening = application.jobOpening
        hiring_company = job_opening.company
        sub_departments = ", ".join(str(value) for value in job_opening.subDepartments) or "None"

        prompt = (
            f"Application ID: {application_id}\n"
            f"Candidate: first_name=\"{application.firstName}\", last_name=\"{application.lastName}\"\n"
            f"Email: {application.email}\n"
            f"Phone: {application.mobile}\n"
            f"Bio: {application.bio}\n"
            f"LinkedIn URL: {application.linkedinUrl}\n"
            f"Job opening title: {job_opening.title}\n"
            f"Job opening seniority level: {job_opening.seniorityLevel}\n"
            f"Job opening department: {job_opening.department}\n"
            f"Job opening sub-departments: {sub_departments}\n"
            f"Job opening description: {job_opening.jobDescription}\n"
            f"Hiring company: {hiring_company.name}\n"
            f"Hiring company site: {hiring_company.siteUrl}\n"
            f"Hiring company size: {hiring_company.size}\n"
            f"Candidate region: {application.region}\n"
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
