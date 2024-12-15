from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import time, date, timedelta

class RepairRequestCreateUpdateSchema(BaseModel):
    request_id: int
    gos_num: Optional[str] = None
    repair_cost: Optional[Decimal] = None
    repair_duration: Optional[timedelta] = None

class RepairRequestSchema(RepairRequestCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    #gos_num: Optional[str] = None