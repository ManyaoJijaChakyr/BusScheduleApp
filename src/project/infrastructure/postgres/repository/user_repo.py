from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, PendingRollbackError, InterfaceError

from project.schemas.user import UserSchema, UserCreateUpdateSchema
from project.infrastructure.postgres.models import User

from project.core.exceptions import UserNotFound, UserAlreadyExists


class UserRepository:
    _collection: Type[User] = User

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.email == email)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=email)

        return UserSchema.model_validate(obj=user)

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = select(self._collection)

        users = await session.scalars(query)

        return [UserSchema.model_validate(obj=user) for user in users.all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == user_id)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=user_id)

        return UserSchema.model_validate(obj=user)

    async def create_user(
        self,
        session: AsyncSession,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            insert(self._collection)
            .values(user.model_dump())
            .returning(self._collection)
        )

        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise UserAlreadyExists(email=user.email)

        return UserSchema.model_validate(obj=created_user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == user_id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise UserNotFound(_id=user_id)

        return UserSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == user_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise UserNotFound(_id=user_id)





'''from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import UserSchema, UserCreateUpdateSchema

from project.core.exceptions import UserNotFound, UserAlreadyExists
from project.api.depends import database, user_repo, get_current_user, check_for_admin_access
from project.resource.auth import get_password_hash

from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, PendingRollbackError, InterfaceError

user_router = APIRouter()


@user_router.get(
    "/all_users",
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_all_users() -> list[UserSchema]:
    async with database.session() as session:
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@user_router.get(
    "/user/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_user_by_id(
    user_id: int,
) -> UserSchema:
    try:
        async with database.session() as session:
            user = await user_repo.get_user_by_id(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


@user_router.post(
    "/add_user",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user_dto: UserCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            user_dto.password = get_password_hash(password=user_dto.password)
            new_user = await user_repo.create_user(session=session, user=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_user


@user_router.put(
    "/update_user/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_dto: UserCreateUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            user_dto.password = get_password_hash(password=user_dto.password)
            updated_user = await user_repo.update_user(
                session=session,
                user_id=user_id,
                user=user_dto,
            )
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_user


@user_router.delete(
    "/delete_user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    current_user: UserSchema = Depends(get_current_user),
) -> None:
    check_for_admin_access(user=current_user)
    try:
        async with database.session() as session:
            user = await user_repo.delete_user(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user'''