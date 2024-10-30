from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.mechanic import MechanicSchema
from project.infrastructure.postgres.models import Mechanic

from project.core.config import settings


class MechanicRepository:
    _collection: Type[Mechanic] = Mechanic

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_mecs(
        self,
        session: AsyncSession,
    ) -> list[MechanicSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.mechanics;"

        mecs = await session.execute(text(query))

        return [MechanicSchema.model_validate(obj=mec) for mec in mecs.mappings().all()]



