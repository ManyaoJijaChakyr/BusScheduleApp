from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.exc import IntegrityError
from project.schemas.company import CompanySchema, CompanyCreateUpdateSchema
from project.infrastructure.postgres.models import Company
from project.core.exceptions import CompanyNotFound

class CompanyRepository:
    _collection: Type[Company] = Company

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_companies(self, session: AsyncSession) -> list[CompanySchema]:
        query = select(self._collection)
        companies = await session.scalars(query)
        return [CompanySchema.model_validate(obj=company) for company in companies.all()]

    async def get_company_by_id(self, session: AsyncSession, id_company: int) -> CompanySchema:
        query = select(self._collection).where(self._collection.id_company == id_company)
        company = await session.scalar(query)
        if not company:
            raise CompanyNotFound(_id_company=id_company)
        return CompanySchema.model_validate(obj=company)

    async def create_company(self, session: AsyncSession, company: CompanyCreateUpdateSchema) -> CompanySchema:
        query = insert(self._collection).values(company.model_dump()).returning(self._collection)
        created_company = await session.scalar(query)
        await session.flush()
        #try:
        #    created_company = await session.scalar(query)
        #    await session.flush()
        #except IntegrityError:
        #    raise CompanyAlreadyExists(company_name=company.company_name)
        return CompanySchema.model_validate(obj=created_company)

    async def update_company(self, session: AsyncSession, id_company: int, company: CompanyCreateUpdateSchema) -> CompanySchema:
        query = update(self._collection).where(self._collection.id_company == id_company).values(company.model_dump()).returning(self._collection)
        updated_company = await session.scalar(query)
        if not updated_company:
            raise CompanyNotFound(_id_company=id_company)
        return CompanySchema.model_validate(obj=updated_company)

    async def delete_company(self, session: AsyncSession, id_company: int) -> None:
        query = delete(self._collection).where(self._collection.id_company == id_company)
        result = await session.execute(query)
        if not result.rowcount:
            raise CompanyNotFound(_id_company=id_company)