from pydantic import BaseModel, ConfigDict
from typing import Optional

class CompanyCreateUpdateSchema(BaseModel):
    company_name: str
    company_address: Optional[str] = None
    phone_number: Optional[str] = None
    employees: Optional[str] = None
    routes_served: Optional[str] = None

class CompanySchema(CompanyCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_company: int