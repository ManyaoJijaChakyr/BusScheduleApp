from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import time
from decimal import Decimal

class RouteCreateUpdateSchema(BaseModel):
    start_stop: Optional[str] = None
    end_stop: Optional[str] = None
    stops_count: Optional[int] = None
    interval: Optional[time] = None
    ticket_price: Optional[Decimal] = None
    first_adv: Optional[time] = None
    last_adv: Optional[time] = None
    stops_list: Optional[str] = None

class RouteSchema(RouteCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    route_number: int