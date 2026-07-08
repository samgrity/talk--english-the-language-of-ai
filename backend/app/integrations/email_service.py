async def send_recruiter_message_to_candidate(
    application_id: str,
    recruiter_id: str,
    correspondence: str,
) -> None:
    # TODO: Replace with real email API integration (SendGrid, Gmail API, etc.).
    # Planned behavior:
    # 1) Resolve the email thread tied to application_id.
    # 2) Send recruiter-authored correspondence as an outbound message.
    # 3) Persist provider metadata for retries/auditing.
    _ = (application_id, recruiter_id, correspondence)
