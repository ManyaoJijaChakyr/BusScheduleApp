from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time


class TripCreateUpdateSchema(BaseModel):
    driver_passport: Optional[str] = None
    route_number: Optional[int] = None
    gos_num: Optional[str] = None
    trip_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class TripSchema(TripCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)