from fastapi import APIRouter

from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.repository.mec_repo import MechanicRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.user import UserSchema
from project.schemas.mechanic import MechanicSchema

router = APIRouter()


@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users() -> list[UserSchema]:
    user_repo = UserRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@router.get("/all_mec", response_model=list[MechanicSchema])
async def get_all_mecs() -> list[MechanicSchema]:
    mec_repo = MechanicRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await mec_repo.check_connection(session=session)
        all_mecs = await mec_repo.get_all_mecs(session=session)

    return all_mecs
