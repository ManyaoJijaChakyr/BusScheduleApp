from pydantic import BaseModel, Field
from typing import Optional

class CompanyCreateUpdateSchema(BaseModel):
    company_name: str
    company_address: Optional[str] = None
    phone_number: Optional[str] = None
    employees: Optional[str] = None
    routes_served: Optional[str] = None

class CompanySchema(CompanyCreateUpdateSchema):
    id_company: int