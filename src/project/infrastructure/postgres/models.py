from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Numeric, Time, Interval, Date, DECIMAL, ForeignKeyConstraint
from datetime import time, date, timedelta
from sqlalchemy import ForeignKey, false
from project.infrastructure.postgres.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())


class Mechanic(Base):
    __tablename__ = "mechanics"

    passport_number: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    experience_years: Mapped[int] = mapped_column(nullable=False)


class Company(Base):
    __tablename__ = "companies"

    id_company: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(nullable=False)
    company_address: Mapped[str | None] = mapped_column(nullable=True)
    phone_number: Mapped[str | None] = mapped_column(nullable=True)
    employees: Mapped[str | None] = mapped_column(nullable=True)
    routes_served: Mapped[str | None] = mapped_column(nullable=True)


#class Route(Base):
#    __tablename__ = "routes"
#
#    route_number: Mapped[int] = mapped_column(primary_key=True)
#    start_stop: Mapped[str | None] = mapped_column(nullable=True)
#    end_stop: Mapped[str | None] = mapped_column(nullable=True)
#    stops_count: Mapped[int | None] = mapped_column(nullable=True)
#    interval: Mapped[time | None] = mapped_column(nullable=True)
#    ticket_price: Mapped[DECIMAL | None] = mapped_column(Numeric(10, 2), nullable=True)
#    first_adv: Mapped[time | None] = mapped_column(nullable=True)
#    last_adv: Mapped[time | None] = mapped_column(nullable=True)
#    stops_list: Mapped[str | None] = mapped_column(nullable=True)
class Route(Base):
    __tablename__ = "routes"
    route_number: Mapped[int] = mapped_column(primary_key=True)
    start_stop: Mapped[str | None] = mapped_column(nullable=True)
    end_stop: Mapped[str | None] = mapped_column(nullable=True)
    stops_count: Mapped[int | None] = mapped_column(nullable=True)
    interval: Mapped[time | None] = mapped_column(nullable=True)
    ticket_price: Mapped[DECIMAL | None] = mapped_column(Numeric(10, 2), nullable=True)
    first_adv: Mapped[time | None] = mapped_column(nullable=True)
    last_adv: Mapped[time | None] = mapped_column(nullable=True)
    stops_list: Mapped[str | None] = mapped_column(nullable=True)

class Stop(Base):
    __tablename__ = "stops"
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    stop_name: Mapped[str | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(nullable=True)


class Driver(Base):
    __tablename__ = "drivers"
    passport_number: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    id_company: Mapped[int | None] = mapped_column(ForeignKey("companies.id_company"), nullable=True)
    experience_years: Mapped[int | None] = mapped_column(nullable=True)
    routes_served: Mapped[str | None] = mapped_column(nullable=True)
    contract_number: Mapped[str | None] = mapped_column(nullable=True)
    contract_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    contract_end: Mapped[date | None] = mapped_column(Date, nullable=True)


#class RouteStop(Base):
#    __tablename__ = "route_stops"
#    latitude: Mapped[float] = mapped_column(Numeric(9, 6), ForeignKey("stops.latitude"), primary_key=True)
#    longitude: Mapped[float] = mapped_column(Numeric(9, 6), ForeignKey("stops.longitude"), primary_key=True)
#    route_number: Mapped[int] = mapped_column(ForeignKey("routes.route_number"), primary_key=True)


class RouteStop(Base):
    __tablename__ = "route_stops"
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    route_number: Mapped[int] = mapped_column(ForeignKey("routes.route_number"), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["latitude", "longitude"], ["stops.latitude", "stops.longitude"]
        ),
    )

#class StopTime(Base):
#    __tablename__ = "stop_time"
#    latitude: Mapped[float] = mapped_column(Numeric(9, 6), ForeignKey("stops.latitude"), primary_key=True)
#    longitude: Mapped[float] = mapped_column(Numeric(9, 6), ForeignKey("stops.longitude"), primary_key=True)
#    route_number: Mapped[int] = mapped_column(ForeignKey("routes.route_number"), primary_key=True)
#    arrival_time: Mapped[time | None] = mapped_column(Time, nullable=True)
#    departure_time: Mapped[time | None] = mapped_column(Time, nullable=True)


class StopTime(Base):
    __tablename__ = "stop_time"
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), primary_key=True)
    route_number: Mapped[int] = mapped_column(ForeignKey("routes.route_number"), primary_key=True)
    arrival_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    departure_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["latitude", "longitude"], ["stops.latitude", "stops.longitude"]
        ),
    )

class Bus(Base):
    __tablename__ = "buses"
    gos_num: Mapped[str] = mapped_column(primary_key=True)
    brand: Mapped[str | None] = mapped_column(nullable=True)
    model: Mapped[str | None] = mapped_column(nullable=True)
    manufacture_year: Mapped[int | None] = mapped_column(nullable=True)
    owner_company: Mapped[int | None] = mapped_column(ForeignKey("companies.id_company"), nullable=True)
    route_number: Mapped[int | None] = mapped_column(ForeignKey("routes.route_number"), nullable=True)
    technical_condition: Mapped[str | None] = mapped_column(nullable=True)
    driver_passport: Mapped[str | None] = mapped_column(ForeignKey("drivers.passport_number"), nullable=True)
    capacity: Mapped[int | None] = mapped_column(nullable=True)
    registration_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class RepairRequest(Base):
    __tablename__ = "repair_requests"
    request_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gos_num: Mapped[str | None] = mapped_column(ForeignKey("buses.gos_num"), nullable=True)
    repair_cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    repair_duration: Mapped[timedelta | None] = mapped_column(Interval, nullable=True)


class TechnicalInspection(Base):
    __tablename__ = "technical_inspections"
    inspection_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mechanic_passport: Mapped[str | None] = mapped_column(ForeignKey("mechanics.passport_number"), nullable=True)
    gos_num: Mapped[str | None] = mapped_column(ForeignKey("buses.gos_num"), nullable=True)
    conclusion: Mapped[str | None] = mapped_column(nullable=True)


class Trip(Base):
    __tablename__ = "trips"
    trip_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_passport: Mapped[str | None] = mapped_column(ForeignKey("drivers.passport_number"), nullable=True)
    route_number: Mapped[int | None] = mapped_column(ForeignKey("routes.route_number"), nullable=True)
    gos_num: Mapped[str | None] = mapped_column(ForeignKey("buses.gos_num"), nullable=True)
    trip_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)