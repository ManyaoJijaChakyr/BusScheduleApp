from pydantic import BaseModel, Field, ConfigDict


#class MechanicSchema(BaseModel):
#    model_config = ConfigDict(from_attributes=True)
#
#    passport_number: str
#    full_name: str
#    experience_years: int

class MecCreateUpdateSchema(BaseModel):
    #first_name: str
    #last_name: str
    #email: str
    #password: str
    #phone_number: str | None = Field(default=None)
    passport_number: str
    full_name: str
    experience_years: int
class MechanicSchema(MecCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    #passport_number: str
