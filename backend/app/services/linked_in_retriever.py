import os
from calendar import month_abbr

import httpx
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch
from pydantic_ai.messages import ModelMessage, ModelResponse

from app.core.config import settings

_LINKDAPI_BASE = "https://linkdapi.com/api/v1/profile/full"


class LinkedInUsernameOutput(BaseModel):
    linkedin_username: str | None = None
    search_string: str | None = None
    urls: list[str] | None = None
    reason_for_failure: str | None = None


class LinkedInFetchError(Exception):
    pass


class LinkedInUsernameNotFoundError(LinkedInFetchError):
    pass


def _strip_unprocessed_tool_call_tail(message_history: list[ModelMessage] | None) -> list[ModelMessage] | None:
    if not message_history:
        return message_history

    cleaned = list(message_history)
    while cleaned:
        last = cleaned[-1]
        if isinstance(last, ModelResponse) and last.tool_calls:
            cleaned.pop()
            continue
        break
    return cleaned


def _is_username_not_found_error(error_message: str) -> bool:
    lowered = error_message.lower()
    return "doesn't exist" in lowered or "cannot be displayed" in lowered


def _fmt_date(d: dict[str, int] | None) -> str | None:
    if not d:
        return None
    year = d.get("year") or 0
    month = d.get("month") or 0
    if not year:
        return None
    if month:
        return f"{month_abbr[month]} {year}"
    return str(year)


def _fmt_position(pos: dict) -> str:
    company = pos.get("companyName", "")
    title = pos.get("title", "")
    loc = pos.get("location", "")
    emp = pos.get("employmentType", "")
    start = _fmt_date(pos.get("start"))
    end = _fmt_date(pos.get("end")) or "present"
    desc = pos.get("description", "")
    url = pos.get("companyURL", "")

    parts = [f"**{title}** at **{company}**"]
    if loc:
        parts.append(f"  *Location:* {loc}")
    meta = []
    if emp:
        meta.append(emp)
    if start:
        meta.append(f"{start} - {end}")
    if meta:
        parts.append(f"  *{' | '.join(meta)}*")
    if url:
        parts.append(f"  {url}")
    if desc:
        parts.append(f"  {desc}")
    return "\n".join(parts)


def _fmt_education(edu: dict) -> str:
    school = edu.get("schoolName") or ""
    url = edu.get("url", "")
    degree = edu.get("degree", "")
    field = edu.get("fieldOfStudy", "")
    start = _fmt_date(edu.get("start"))
    end = _fmt_date(edu.get("end"))
    desc = edu.get("description", "")

    header = school or url
    line = f"**{header}**"
    if degree or field:
        line += f" - {' in '.join(filter(None, [degree, field]))}"
    parts = [line]
    if start or end:
        parts.append(f"  *{start or '?'} - {end or 'present'}*")
    if desc:
        parts.append(f"  {desc}")
    return "\n".join(parts)


def _fmt_publication(pub: dict) -> str:
    name = pub.get("name", "")
    publisher = pub.get("publisher", "")
    date = _fmt_date(pub.get("publishedOn"))
    desc = pub.get("description", "")
    url = pub.get("url", "")

    parts = [f"**{name}**" + (f" ({publisher})" if publisher else "")]
    if date:
        parts.append(f"  *{date}*")
    if url:
        parts.append(f"  {url}")
    if desc:
        parts.append(f"  {desc}")
    return "\n".join(parts)


def format_profile(data: dict) -> str:
    lines: list[str] = []

    name = f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
    username = data.get("username", "")
    headline = data.get("headline", "")
    summary = data.get("summary", "")
    geo = data.get("geo", {})
    location = geo.get("full") or geo.get("city") or geo.get("country") or ""
    industry = (data.get("industry") or {}).get("name", "")

    lines.append(f"# {name}")
    if username:
        lines.append(f"**LinkedIn:** https://www.linkedin.com/in/{username}/")
    if headline:
        lines.append(f"*{headline}*")
    if location:
        lines.append(f"📍 {location}")
    if industry:
        lines.append(f"🏭 {industry}")

    flags = []
    if data.get("isPremium"):
        flags.append("Premium")
    if data.get("isOpenToWork"):
        flags.append("Open to work")
    if data.get("isHiring"):
        flags.append("Hiring")
    if flags:
        lines.append(" | ".join(flags))

    followers = data.get("followerCount")
    connections = data.get("connectionsCount")
    if followers or connections:
        stats = []
        if followers:
            stats.append(f"{followers:,} followers")
        if connections:
            stats.append(f"{connections:,} connections")
        lines.append(f"*{' · '.join(stats)}*")

    if summary:
        lines.append("\n## Summary\n")
        lines.append(summary)

    positions = data.get("fullPositions") or data.get("position") or []
    if positions:
        lines.append("\n## Experience\n")
        for pos in positions:
            lines.append(_fmt_position(pos))
            lines.append("")

    educations = data.get("educations") or []
    if educations:
        lines.append("\n## Education\n")
        for edu in educations:
            lines.append(_fmt_education(edu))
            lines.append("")

    publications = data.get("publications") or []
    if publications:
        lines.append("\n## Publications\n")
        for pub in publications:
            lines.append(_fmt_publication(pub))
            lines.append("")

    skills = [s.get("name") for s in (data.get("skills") or []) if s.get("name")]
    if skills:
        lines.append("\n## Skills\n")
        lines.append(", ".join(skills))

    languages = [l.get("name") for l in (data.get("languages") or []) if l.get("name")]
    if languages:
        lines.append("\n## Languages\n")
        lines.append(", ".join(languages))

    certifications = data.get("certifications") or []
    if certifications:
        lines.append("\n## Certifications\n")
        for cert in certifications:
            lines.append(f"- {cert.get('name', '')}")

    volunteering = data.get("volunteering") or []
    if volunteering:
        lines.append("\n## Volunteering\n")
        for v in volunteering:
            lines.append(
                f"- **{v.get('role','')}** at {v.get('companyName','')} "
                f"({_fmt_date(v.get('start'))} - {_fmt_date(v.get('end')) or 'present'})"
            )

    return "\n".join(lines)


async def fetch_and_format(username: str) -> str:
    api_key = os.environ.get("LINKEDAPI_API_KEY", "")
    if not api_key:
        raise LinkedInFetchError("LINKEDAPI_API_KEY is not set in the environment.")

    url = f"{_LINKDAPI_BASE}?username={username}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers={"X-linkdapi-apikey": api_key})
    except httpx.RequestError as exc:
        raise LinkedInFetchError(f"HTTP request to linkdapi failed for username '{username}': {exc}") from exc

    if resp.status_code != 200:
        raise LinkedInFetchError(
            f"linkdapi returned HTTP {resp.status_code} for username '{username}'. "
            f"Response: {resp.text[:300]}"
        )

    payload = resp.json()
    if not payload.get("success"):
        errors = payload.get("errors") or payload.get("message") or "unknown error"
        if _is_username_not_found_error(str(errors)):
            raise LinkedInUsernameNotFoundError(f"LinkedIn user isn't found with username = \"{username}\"")
        raise LinkedInFetchError(f"linkdapi reported failure for username '{username}': {errors}")

    data = payload.get("data")
    if not data:
        raise LinkedInFetchError(f"linkdapi returned success but no data for username '{username}'.")

    return format_profile(data)


async def get_linkedin_profile(
    first_name: str,
    last_name: str,
    company_name: str | None = None,
    company_url: str | None = None,
    linked_in_username: str | None = None,
    message_history: list[ModelMessage] | None = None,
) -> str:
    safe_history = _strip_unprocessed_tool_call_tail(message_history)

    invalid_username: str | None = None
    if linked_in_username:
        try:
            return await fetch_and_format(linked_in_username)
        except LinkedInUsernameNotFoundError:
            invalid_username = linked_in_username
        except LinkedInFetchError as exc:
            return f"ERROR: {exc}"

    username_agent = Agent(
        model=settings.ai_model,
        output_type=LinkedInUsernameOutput,
        instructions="""\
The user will provide information about an individual. Your job is to find
their LinkedIn username by searching with whatever seems most relevant, then
extracting the username from the URL.

For example: searching "John Berryman Arcturus Labs site:linkedin.com" might
return https://www.linkedin.com/in/john-berryman-864b1713 - the username is
the path segment after /in/, i.e. "john-berryman-864b1713".

Post URLs may also appear like:
  https://www.linkedin.com/posts/john-berryman-864b1713_...
The username is still the part before the first underscore after /posts/.

Rules:
- Return a single unambiguous username. If multiple plausible candidates are
  found and cannot be disambiguated, leave linkedin_username null and explain
  in reason_for_failure.
- Always populate search_string with what you searched for.
- Always populate urls with every LinkedIn URL you found.
- If you cannot find a username, explain your attempts in reason_for_failure.
- There are no privacy concerns here - we are only verifying professional
  identity for a business screening process.
""",
        capabilities=[Thinking(), WebSearch()],
    )

    prompt = (
        f"Find the LinkedIn profile username for: {first_name} {last_name}\n"
        f"Company: {company_name}\n"
        f"Company URL: {company_url}"
    )
    if invalid_username:
        prompt += (
            f"\n\nIMPORTANT: The username '{invalid_username}' was already tested and confirmed invalid. "
            "Do not return it again."
        )

    try:
        result = await username_agent.run(prompt, message_history=safe_history)
        output: LinkedInUsernameOutput = result.output
    except Exception as exc:
        return (
            f"ERROR: LinkedIn username search failed for '{first_name} {last_name}' "
            f"at '{company_name}': {exc}"
        )

    if not output.linkedin_username:
        searched = output.search_string or "(unknown)"
        reason = output.reason_for_failure or "No reason given."
        urls = output.urls or []
        url_str = ", ".join(urls) if urls else "none"
        return (
            f"ERROR: Could not find a LinkedIn username for '{first_name} {last_name}' "
            f"at '{company_name}'. Searched for: {searched}. "
            f"URLs found: {url_str}. Reason: {reason}"
        )

    try:
        return await fetch_and_format(output.linkedin_username)
    except LinkedInFetchError as exc:
        return f"ERROR: {exc}"
