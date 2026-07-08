from typing import Protocol

from app.db.models.recruiter import RecruiterModel


class RecruiterRepository(Protocol):
    async def list_all(self) -> list[RecruiterModel]: ...

    async def get_name_map(self) -> dict[str, str]: ...
