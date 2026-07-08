from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.recruiter import RecruiterModel


class SqlAlchemyRecruiterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> list[RecruiterModel]:
        result = await self.session.execute(select(RecruiterModel))
        return list(result.scalars().all())

    async def get_name_map(self) -> dict[str, str]:
        recruiters = await self.list_all()
        return {recruiter.id: recruiter.name for recruiter in recruiters}
