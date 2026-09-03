
from pydantic import BaseModel, Field
from typing import Optional


class Employee(BaseModel):
    id:int =Field(..., description="The unique identifier for the employee")
    name:str = Field(..., max_length=100, min_length=2, description="The name of the employee")
    salary:float =Field(...,gt=0, description="The salary of the employee")
    department:str =Field(...,max_length=50, description="The department of the employee")

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, min_length=2, description="The name of the employee")
    salary: Optional[float] = Field(None, gt=0, description="The salary of the employee")
    department: Optional[str] = Field(None, max_length=50, description="The department of the employee")
