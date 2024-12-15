from pydantic import BaseModel, ConfigDict
from datetime import time
from typing import Optional

class StopTimeCreateUpdateSchema(BaseModel):
    latitude: float
    longitude: float
    route_number: int
    arrival_time: Optional[time] = None
    departure_time: Optional[time] = None

class StopTimeSchema(StopTimeCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
