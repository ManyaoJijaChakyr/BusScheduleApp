from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

class RepairRequestCreateUpdateSchema(BaseModel):
    gos_num: Optional[str] = None
    repair_cost: Optional[Decimal] = None
    repair_duration: Optional[str] = None

class RepairRequestSchema(RepairRequestCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)