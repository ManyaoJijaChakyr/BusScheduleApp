from fastapi import APIRouter, HTTPException, status

#from project.infrastructure.postgres.repository.user_repo import UserRepository
#from project.infrastructure.postgres.repository.mec_repo import MechanicRepository
#from project.infrastructure.postgres.database import PostgresDatabase
#from project.schemas.user import UserSchema
from project.schemas.mechanic import MechanicSchema, MecCreateUpdateSchema
from project.schemas.company import CompanySchema, CompanyCreateUpdateSchema
from project.schemas.route import RouteSchema, RouteCreateUpdateSchema
from project.schemas.stop import StopSchema, StopCreateUpdateSchema
from project.schemas.driver import DriverSchema, DriverCreateUpdateSchema
from project.schemas.stop_time import StopTimeSchema, StopTimeCreateUpdateSchema
from project.schemas.route_stop import RouteStopSchema, RouteStopCreateUpdateSchema
from project.schemas.bus import BusSchema, BusCreateUpdateSchema
from project.schemas.repair_request import RepairRequestSchema, RepairRequestCreateUpdateSchema
from project.schemas.technical_inspection import TechnicalInspectionSchema, TechnicalInspectionCreateUpdateSchema
from project.schemas.trip import TripSchema, TripCreateUpdateSchema

from project.core.exceptions import MecNotFound, MecAlreadyExists
from project.core.exceptions import CompanyAlreadyExists, CompanyNotFound
from project.core.exceptions import RouteNotFound, RouteAlreadyExists
from project.core.exceptions import StopAlreadyExists, StopNotFound
from project.core.exceptions import DriverAlreadyExists, DriverNotFound
from project.core.exceptions import StopTimeNotFound, StopTimeAlreadyExists
from project.core.exceptions import RouteStopNotFound, RouteStopAlreadyExists
from project.core.exceptions import BusNotFound, BusAlreadyExists
from project.core.exceptions import RepairRequestAlreadyExists, RepairRequestNotFound
from project.core.exceptions import TechnicalInspectionNotFound, TechnicalInspectionAlreadyExists
from project.core.exceptions import TripNotFound, TripAlreadyExists

from project.api.depends import (database, mec_repo, company_repo, route_repo, stop_repo, driver_repo, stop_time_repo,
                                 route_stop_repo, bus_repo, repair_request_repo, technical_inspection_repo, trip_repo)



router = APIRouter()


#@router.get("/all_users", response_model=list[UserSchema])
#async def get_all_users() -> list[UserSchema]:
#    user_repo = UserRepository()
#    database = PostgresDatabase()
#
#    async with database.session() as session:
#        await user_repo.check_connection(session=session)
#        all_users = await user_repo.get_all_users(session=session)
#
#    return all_users

@router.get("/all_mecs", response_model=list[MechanicSchema], status_code=status.HTTP_200_OK)
async def get_all_mecs() -> list[MechanicSchema]:
    async with database.session() as session:
        all_mecs = await mec_repo.get_all_mecs(session=session)

    return all_mecs

@router.get("/mec/{passport_number}", response_model=MechanicSchema, status_code=status.HTTP_200_OK)
async def get_mec_by_p_n(
    passport_number: str,
) -> MechanicSchema:
    try:
        async with database.session() as session:
            mec = await mec_repo.get_mec_by_p_n(session=session, passport_number=passport_number)
    except MecNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return mec
@router.post("/add_mec", response_model=MechanicSchema, status_code=status.HTTP_201_CREATED)
async def add_mec(
    mec_dto: MecCreateUpdateSchema,
) -> MechanicSchema:
    try:
        async with database.session() as session:
            new_mec = await mec_repo.create_mec(session=session, mec=mec_dto)
    except MecAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_mec
@router.put(
    "/update_mec/{passport_number}",
    response_model=MechanicSchema,
    status_code=status.HTTP_200_OK,
)
async def update_mec(
    passport_number: str,
    mec_dto: MecCreateUpdateSchema,
) -> MechanicSchema:
    try:
        async with database.session() as session:
            updated_mec = await mec_repo.update_mec(
                session=session,
                passport_number=passport_number,
                mec=mec_dto,
            )
    except MecNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_mec

@router.delete("/delete_mec/{passport_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mec(
    passport_number: str,
) -> None:
    try:
        async with database.session() as session:
            mec = await mec_repo.delete_mec(session=session, passport_number=passport_number)
    except MecNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return mec


@router.get("/all_companies", response_model=list[CompanySchema], status_code=status.HTTP_200_OK)
async def get_all_companies() -> list[CompanySchema]:
    async with database.session() as session:
        all_companies = await company_repo.get_all_companies(session=session)
    return all_companies

@router.get("/company/{id_company}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def get_company_by_id(id_company: int) -> CompanySchema:
    try:
        async with database.session() as session:
            company = await company_repo.get_company_by_id(session=session, id_company=id_company)
    except CompanyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return company

@router.post("/add_company", response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def add_company(company_dto: CompanyCreateUpdateSchema) -> CompanySchema:
    try:
        async with database.session() as session:
            new_company = await company_repo.create_company(session=session, company=company_dto)
    except CompanyAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_company

@router.put("/update_company/{id_company}", response_model=CompanySchema, status_code=status.HTTP_200_OK)
async def update_company(id_company: int, company_dto: CompanyCreateUpdateSchema) -> CompanySchema:
    try:
        async with database.session() as session:
            updated_company = await company_repo.update_company(session=session, id_company=id_company, company=company_dto)
    except CompanyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_company

@router.delete("/delete_company/{id_company}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(id_company: int) -> None:
    try:
        async with database.session() as session:
            company = await company_repo.delete_company(session=session, id_company=id_company)
    except CompanyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return None

@router.get("/all_routes", response_model=list[RouteSchema], status_code=status.HTTP_200_OK)
async def get_all_routes() -> list[RouteSchema]:
    async with database.session() as session:
        all_routes = await route_repo.get_all_routes(session=session)
    return all_routes

@router.get("/route/{route_number}", response_model=RouteSchema, status_code=status.HTTP_200_OK)
async def get_route_by_route_number(route_number: int) -> RouteSchema:
    try:
        async with database.session() as session:
            route = await route_repo.get_route_by_number(session=session, route_number=route_number)
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return route

@router.post("/add_route", response_model=RouteSchema, status_code=status.HTTP_201_CREATED)
async def add_route(route_dto: RouteCreateUpdateSchema) -> RouteSchema:
    try:
        async with database.session() as session:
            new_route = await route_repo.create_route(session=session, route=route_dto)
    except RouteAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_route

@router.put("/update_route/{route_number}", response_model=RouteSchema, status_code=status.HTTP_200_OK)
async def update_route(route_number: int, route_dto: RouteCreateUpdateSchema) -> RouteSchema:
    try:
        async with database.session() as session:
            updated_route = await route_repo.update_route(session=session, route_number=route_number, route=route_dto)
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_route

@router.delete("/delete_route/{route_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(route_number: int) -> None:
    try:
        async with database.session() as session:
            route = await route_repo.delete_route(session=session, route_number=route_number)
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return None

@router.get("/all_stops", response_model=list[StopSchema], status_code=status.HTTP_200_OK)
async def get_all_stops() -> list[StopSchema]:
    async with database.session() as session:
        all_stops = await stop_repo.get_all_stops(session=session)
    return all_stops

@router.get("/stop/{latitude}/{longitude}", response_model=StopSchema, status_code=status.HTTP_200_OK)
async def get_stop_by_coordinates(latitude: float, longitude: float) -> StopSchema:
    try:
        async with database.session() as session:
            stop = await stop_repo.get_stop_by_coordinates(session=session, latitude=latitude, longitude=longitude)
    except StopNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return stop

@router.post("/add_stop", response_model=StopSchema, status_code=status.HTTP_201_CREATED)
async def add_stop(stop_dto: StopCreateUpdateSchema) -> StopSchema:
    try:
        async with database.session() as session:
            new_stop = await stop_repo.create_stop(session=session, stop=stop_dto)
    except StopAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_stop

@router.put("/update_stop/{latitude}/{longitude}", response_model=StopSchema, status_code=status.HTTP_200_OK)
async def update_stop(latitude: float, longitude: float, stop_dto: StopCreateUpdateSchema) -> StopSchema:
    try:
        async with database.session() as session:
            updated_stop = await stop_repo.update_stop(session=session, latitude=latitude, longitude=longitude, stop=stop_dto)
    except StopNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_stop

@router.delete("/delete_stop/{latitude}/{longitude}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(latitude: float, longitude: float) -> None:
    try:
        async with database.session() as session:
            stop = await stop_repo.delete_stop(session=session, latitude=latitude, longitude=longitude)
    except StopNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return None


@router.get("/all_drivers", response_model=list[DriverSchema], status_code=status.HTTP_200_OK)
async def get_all_drivers() -> list[DriverSchema]:
    async with database.session() as session:
        all_drivers = await driver_repo.get_all_drivers(session=session)
    return all_drivers

@router.get("/driver/{passport_number}", response_model=DriverSchema, status_code=status.HTTP_200_OK)
async def get_driver_by_passport_number(passport_number: str) -> DriverSchema:
    try:
        async with database.session() as session:
            driver = await driver_repo.get_driver_by_passport_number(session=session, passport_number=passport_number)
    except DriverNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return driver

@router.post("/add_driver", response_model=DriverSchema, status_code=status.HTTP_201_CREATED)
async def add_driver(driver_dto: DriverCreateUpdateSchema) -> DriverSchema:
    try:
        async with database.session() as session:
            new_driver = await driver_repo.create_driver(session=session, driver=driver_dto)
    except DriverAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_driver

@router.put("/update_driver/{passport_number}", response_model=DriverSchema, status_code=status.HTTP_200_OK)
async def update_driver(passport_number: str, driver_dto: DriverCreateUpdateSchema) -> DriverSchema:
    try:
        async with database.session() as session:
            updated_driver = await driver_repo.update_driver(session=session, passport_number=passport_number, driver=driver_dto)
    except DriverNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_driver

@router.delete("/delete_driver/{passport_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(passport_number: str) -> None:
    try:
        async with database.session() as session:
            await driver_repo.delete_driver(session=session, passport_number=passport_number)
    except DriverNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/all_stop_times", response_model=list[StopTimeSchema], status_code=status.HTTP_200_OK)
async def get_all_stop_times() -> list[StopTimeSchema]:
    async with database.session() as session:
        all_stop_times = await stop_time_repo.get_all_stop_times(session=session)
    return all_stop_times

@router.post("/add_stop_time", response_model=StopTimeSchema, status_code=status.HTTP_201_CREATED)
async def add_stop_time(stop_time_dto: StopTimeCreateUpdateSchema) -> StopTimeSchema:
    try:
        async with database.session() as session:
            new_stop_time = await stop_time_repo.create_stop_time(session=session, stop_time=stop_time_dto)
    except StopTimeAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_stop_time


@router.delete("/delete_stop_time/{latitude}/{longitude}/{route_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop_time(latitude: float, longitude: float, route_number: int) -> None:
    try:
        async with database.session() as session:
            await stop_time_repo.delete_stop_time(session=session, latitude=latitude, longitude=longitude, route_number=route_number)
    except StopTimeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/all_route_stops", response_model=list[RouteStopSchema], status_code=status.HTTP_200_OK)
async def get_all_route_stops() -> list[RouteStopSchema]:
    async with database.session() as session:
        all_route_stops = await route_stop_repo.get_all_route_stops(session=session)
    return all_route_stops

@router.post("/add_route_stop", response_model=RouteStopSchema, status_code=status.HTTP_201_CREATED)
async def add_route_stop(route_stop_dto: RouteStopCreateUpdateSchema) -> RouteStopSchema:
    try:
        async with database.session() as session:
            new_route_stop = await route_stop_repo.create_route_stop(session=session, route_stop=route_stop_dto)
    except RouteStopAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_route_stop

@router.delete("/delete_route_stop/{latitude}/{longitude}/{route_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route_stop(latitude: float, longitude: float, route_number: int) -> None:
    try:
        async with database.session() as session:
            await route_stop_repo.delete_route_stop(session=session, latitude=latitude, longitude=longitude, route_number=route_number)
    except RouteStopNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/all_buses", response_model=list[BusSchema], status_code=status.HTTP_200_OK)
async def get_all_buses() -> list[BusSchema]:
    async with database.session() as session:
        all_buses = await bus_repo.get_all_buses(session=session)
    return all_buses

@router.get("/bus/{gos_num}", response_model=BusSchema, status_code=status.HTTP_200_OK)
async def get_bus_by_gos_num(gos_num: str) -> BusSchema:
    try:
        async with database.session() as session:
            bus = await bus_repo.get_bus_by_gos_num(session=session, gos_num=gos_num)
    except BusNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bus

@router.post("/add_bus", response_model=BusSchema, status_code=status.HTTP_201_CREATED)
async def add_bus(bus_dto: BusCreateUpdateSchema) -> BusSchema:
    try:
        async with database.session() as session:
            new_bus = await bus_repo.create_bus(session=session, bus=bus_dto)
    except BusAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_bus

@router.put("/update_bus/{gos_num}", response_model=BusSchema, status_code=status.HTTP_200_OK)
async def update_bus(gos_num: str, bus_dto: BusCreateUpdateSchema) -> BusSchema:
    try:
        async with database.session() as session:
            updated_bus = await bus_repo.update_bus(session=session, gos_num=gos_num, bus=bus_dto)
    except BusNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_bus

@router.delete("/delete_bus/{gos_num}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus(gos_num: str) -> None:
    try:
        async with database.session() as session:
            await bus_repo.delete_bus(session=session, gos_num=gos_num)
    except BusNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/all_requests", response_model=list[RepairRequestSchema], status_code=status.HTTP_200_OK)
async def get_all_requests() -> list[RepairRequestSchema]:
    async with database.session() as session:
        all_requests = await repair_request_repo.get_all_requests(session=session)
    return all_requests

@router.get("/request/{request_id}", response_model=RepairRequestSchema, status_code=status.HTTP_200_OK)
async def get_request_by_id(request_id: int) -> RepairRequestSchema:
    try:
        async with database.session() as session:
            request = await repair_request_repo.get_request_by_id(session=session, request_id=request_id)
    except RepairRequestNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return request

@router.post("/add_request", response_model=RepairRequestSchema, status_code=status.HTTP_201_CREATED)
async def add_request(request_dto: RepairRequestCreateUpdateSchema) -> RepairRequestSchema:
    try:
        async with database.session() as session:
            new_request = await repair_request_repo.create_request(session=session, request=request_dto)
    except RepairRequestAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_request

@router.put("/update_request/{request_id}", response_model=RepairRequestSchema, status_code=status.HTTP_200_OK)
async def update_request(request_id: int, request_dto: RepairRequestCreateUpdateSchema) -> RepairRequestSchema:
    try:
        async with database.session() as session:
            updated_request = await repair_request_repo.update_request(session=session, request_id=request_id, mec=request_dto)
    except RepairRequestNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_request

@router.delete("/delete_request/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(request_id: int) -> None:
    try:
        async with database.session() as session:
            await repair_request_repo.delete_request(session=session, request_id=request_id)
    except RepairRequestNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@router.get("/all_inspections", response_model=list[TechnicalInspectionSchema], status_code=status.HTTP_200_OK)
async def get_all_inspections() -> list[TechnicalInspectionSchema]:
    async with database.session() as session:
        all_inspections = await technical_inspection_repo.get_all_inspections(session=session)
    return all_inspections

@router.get("/inspection/{inspection_id}", response_model=TechnicalInspectionSchema, status_code=status.HTTP_200_OK)
async def get_inspection_by_id(inspection_id: int) -> TechnicalInspectionSchema:
    try:
        async with database.session() as session:
            inspection = await technical_inspection_repo.get_inspection_by_id(session=session, inspection_id=inspection_id)
    except TechnicalInspectionNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return inspection

@router.post("/add_inspection", response_model=TechnicalInspectionSchema, status_code=status.HTTP_201_CREATED)
async def add_inspection(inspection_dto: TechnicalInspectionCreateUpdateSchema) -> TechnicalInspectionSchema:
    try:
        async with database.session() as session:
            new_inspection = await technical_inspection_repo.create_inspection(session=session, inspection=inspection_dto)
    except TechnicalInspectionAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_inspection

@router.put("/update_inspection/{inspection_id}", response_model=TechnicalInspectionSchema, status_code=status.HTTP_200_OK)
async def update_inspection(inspection_id: int, inspection_dto: TechnicalInspectionCreateUpdateSchema) -> TechnicalInspectionSchema:
    try:
        async with database.session() as session:
            updated_inspection = await technical_inspection_repo.update_inspection(session=session, inspection_id=inspection_id, inspection=inspection_dto)
    except TechnicalInspectionNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_inspection

@router.delete("/delete_inspection/{inspection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inspection(inspection_id: int) -> None:
    try:
        async with database.session() as session:
            await technical_inspection_repo.delete_inspection(session=session, inspection_id=inspection_id)
    except TechnicalInspectionNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

@router.get("/all_trips", response_model=list[TripSchema], status_code=status.HTTP_200_OK)
async def get_all_trips() -> list[TripSchema]:
    async with database.session() as session:
        all_trips = await trip_repo.get_all_trips(session=session)
    return all_trips

@router.get("/trip/{trip_id}", response_model=TripSchema, status_code=status.HTTP_200_OK)
async def get_trip_by_id(trip_id: int) -> TripSchema:
    try:
        async with database.session() as session:
            trip = await trip_repo.get_trip_by_id(session=session, trip_id=trip_id)
    except TripNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return trip

@router.post("/add_trip", response_model=TripSchema, status_code=status.HTTP_201_CREATED)
async def add_trip(trip_dto: TripCreateUpdateSchema) -> TripSchema:
    try:
        async with database.session() as session:
            new_trip = await trip_repo.create_trip(session=session, trip=trip_dto)
    except TripAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_trip

@router.put("/update_trip/{trip_id}", response_model=TripSchema, status_code=status.HTTP_200_OK)
async def update_trip(trip_id: int, trip_dto: TripCreateUpdateSchema) -> TripSchema:
    try:
        async with database.session() as session:
            updated_trip = await trip_repo.update_trip(session=session, trip_id=trip_id, trip=trip_dto)
    except TripNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_trip

@router.delete("/delete_trip/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: int) -> None:
    try:
        async with database.session() as session:
            await trip_repo.delete_trip(session=session, trip_id=trip_id)
    except TripNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)