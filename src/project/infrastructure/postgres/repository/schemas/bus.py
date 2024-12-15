from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

class BusCreateUpdateSchema(BaseModel):
    gos_num: str
    brand: Optional[str] = None
    model: Optional[str] = None
    manufacture_year: Optional[int] = None
    owner_company: Optional[int] = None
    route_number: Optional[int] = None
    technical_condition: Optional[str] = None
    driver_passport: Optional[str] = None
    capacity: Optional[int] = None
    registration_date: Optional[date] = None

class BusSchema(BusCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)