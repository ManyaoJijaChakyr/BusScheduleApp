from pydantic import BaseModel, ConfigDict
from typing import Optional

class RouteStopCreateUpdateSchema(BaseModel):
    latitude: float
    longitude: float
    route_number: int

class RouteStopSchema(RouteStopCreateUpdateSchema):
    class Config:
        model_config = ConfigDict(from_attributes=True)