from typing import Annotated
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from project.schemas.auth import TokenData
from project.schemas.user import UserSchema
from project.core.config import settings
from project.core.exceptions import CredentialsException

from project.infrastructure.postgres.repository.user_repo import UserRepository
from project.infrastructure.postgres.repository.mec_repo import MechanicRepository
from project.infrastructure.postgres.repository.company_repo import CompanyRepository
from project.infrastructure.postgres.repository.route_repo import RouteRepository
from project.infrastructure.postgres.repository.stop_repo import StopRepository
from project.infrastructure.postgres.repository.driver_repo import DriverRepository
from project.infrastructure.postgres.repository.stop_time_repo import StopTimeRepository
from project.infrastructure.postgres.repository.route_stop_repo import RouteStopRepository
from project.infrastructure.postgres.repository.bus_repo import BusRepository
from project.infrastructure.postgres.repository.repair_request_repo import RepairRequestRepository
from project.infrastructure.postgres.repository.technical_inspection_repo import TechnicalInspectionRepository
from project.infrastructure.postgres.repository.trip_repo import TripRepository

from project.resource.auth import oauth2_scheme
from project.infrastructure.postgres.database import PostgresDatabase

mec_repo = MechanicRepository()
user_repo = UserRepository()
company_repo = CompanyRepository()
route_repo = RouteRepository()
stop_repo = StopRepository()
driver_repo = DriverRepository()
stop_time_repo = StopTimeRepository()
route_stop_repo = RouteStopRepository()
bus_repo = BusRepository()
repair_request_repo = RepairRequestRepository()
technical_inspection_repo = TechnicalInspectionRepository()
trip_repo = TripRepository()

database = PostgresDatabase()

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные для авторизации"
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
    async with database.session() as session:
        user = await user_repo.get_user_by_email(
            session=session,
            email=token_data.username,
        )
    if user is None:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
    return user
def check_for_admin_access(user: UserSchema) -> None:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только админ имеет права добавлять/изменять/удалять пользователей"
        )