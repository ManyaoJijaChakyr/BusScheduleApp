from pydantic import BaseModel, ConfigDict
from typing import Optional

class StopCreateUpdateSchema(BaseModel):
    stop_name: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float

class StopSchema(StopCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    #latitude: float
    #longitude: float