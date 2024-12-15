from pydantic import BaseModel
from typing import Optional

class StopCreateUpdateSchema(BaseModel):
    stop_name: Optional[str] = None
    address: Optional[str] = None

class StopSchema(StopCreateUpdateSchema):
    latitude: float
    longitude: float