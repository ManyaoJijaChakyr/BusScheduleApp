from pydantic import BaseModel, ConfigDict
from typing import Optional

class TechnicalInspectionCreateUpdateSchema(BaseModel):
    mechanic_passport: Optional[str] = None
    gos_num: Optional[str] = None
    conclusion: Optional[str] = None

class TechnicalInspectionSchema(TechnicalInspectionCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)