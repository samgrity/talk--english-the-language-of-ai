from pydantic import BaseModel


class CandidateCorrespondenceHookRequest(BaseModel):
    application_id: str
    correspondence: str


class TriggerAIScreenHookRequest(BaseModel):
    application_id: str
