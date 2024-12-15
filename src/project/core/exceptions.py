from typing import Final


from fastapi import HTTPException, status
class UserNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "User с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class UserAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Пользователь с почтой '{email}' уже существует"

    def __init__(self, email: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(email=email)
        super().__init__(self.message)


class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Произошла ошибка в базе данных: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)


class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
class MecNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Mechanic с passport_number {passport_number} не найден"
    message: str
    def __init__(self, _passport_number: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(passport_number=_passport_number)
        super().__init__(self.message)
class MecAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Механик с паспортом '{passport_number}' уже существует"
    def __init__(self, passport_number: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(passport_number=passport_number)
        super().__init__(self.message)

class CompanyNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Company с id {id} не найден"
    message: str
    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)

class CompanyAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Company с id '{id}' уже существует"
    def __init__(self, id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=id)
        super().__init__(self.message)

class RouteNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Route с route_number {route_number} не найден"
    message: str
    def __init__(self, _route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(route_number=_route_number)
        super().__init__(self.message)

class RouteAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Route с route_number '{route_number}' уже существует"
    def __init__(self, route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(route_number=route_number)
        super().__init__(self.message)

class StopNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Stop с longitude={longitude}, latitude={latitude} не найден"
    message: str
    def __init__(self, _longitude: float, _latitude: float) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(longitude=_longitude, latitude=_latitude)
        super().__init__(self.message)

class StopAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Stop с longitude={longitude}, latitude={latitude} уже существует"
    def __init__(self, longitude: float, latitude: float) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(longitude=longitude, latitude=latitude)
        super().__init__(self.message)


class DriverNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Driver с passport_number {passport_number} не найден"
    message: str
    def __init__(self, _passport_number: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(passport_number=_passport_number)
        super().__init__(self.message)

class DriverAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Driver с passport_number '{passport_number}' уже существует"
    def __init__(self, passport_number: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(passport_number=passport_number)
        super().__init__(self.message)


class StopTimeNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о Route={route_number} остановившемся на Stop с координатами longitude={longitude}, latitude={latitude} не найдена"
    message: str

    def __init__(self, _longitude: float, _latitude: float, _route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(longitude=_longitude, latitude=_latitude, route_number=_route_number)
        super().__init__(self.message)

class StopTimeAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Запись о Route={route_number} остановившемся на Stop с координатами longitude={longitude}, latitude={latitude} уже существует"
    message: str

    def __init__(self, longitude: float, latitude: float, route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(longitude=longitude, latitude=latitude, route_number=route_number)
        super().__init__(self.message)

class RouteStopNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Stop с координатами longitude={longitude}, latitude={latitude} на Route={route_number} не найдена"
    message: str

    def __init__(self, _latitude: float, _longitude: float, _route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(latitude=_latitude, longitude=_longitude, route_number=_route_number)
        super().__init__(self.message)

class RouteStopAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Stop с координатами longitude={longitude}, latitude={latitude} на Route={route_number} уже существует"
    message: str

    def __init__(self, latitude: float, longitude: float, route_number: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(latitude=latitude, longitude=longitude, route_number=route_number)
        super().__init__(self.message)


class BusNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Bus с gos_num {gos_num} не найден"
    message: str
    def __init__(self, _gos_num: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(gos_num=_gos_num)
        super().__init__(self.message)

class BusAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Bus с gos_num '{gos_num}' уже существует"
    def __init__(self, gos_num: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(gos_num=gos_num)
        super().__init__(self.message)


class RepairRequestNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Repair Request с request_id {request_id} не найден"
    message: str
    def __init__(self, _request_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(request_id=_request_id)
        super().__init__(self.message)

class RepairRequestAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Repair Request с request_id {request_id} уже существует"
    def __init__(self, request_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(request_id=request_id)
        super().__init__(self.message)


class TechnicalInspectionNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Technical Inspection с inspection_id {inspection_id} не найден"
    message: str
    def __init__(self, _inspection_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(inspection_id=_inspection_id)
        super().__init__(self.message)

class TechnicalInspectionAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Technical Inspection с inspection_id {inspection_id} уже существует"
    def __init__(self, inspection_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(inspection_id=inspection_id)
        super().__init__(self.message)


class TripNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Trip с trip_id {trip_id} не найден"
    message: str
    def __init__(self, _trip_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(trip_id=_trip_id)
        super().__init__(self.message)

class TripAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Trip с trip_id {trip_id} уже существует"
    def __init__(self, trip_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(trip_id=trip_id)
        super().__init__(self.message)