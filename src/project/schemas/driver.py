from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

class DriverCreateUpdateSchema(BaseModel):
    full_name: str
    id_company: Optional[int] = None
    experience_years: Optional[int] = None
    routes_served: Optional[str] = None
    contract_number: Optional[str] = None
    contract_start: Optional[date] = None
    contract_end: Optional[date] = None
    passport_number: str

class DriverSchema(DriverCreateUpdateSchema):
    #passport_number: str

    model_config = ConfigDict(from_attributes=True)