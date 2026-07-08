from pydantic import BaseModel


class Recruiter(BaseModel):
    id: str
    name: str
