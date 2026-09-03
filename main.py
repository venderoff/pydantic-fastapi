from fastapi    import FastAPI, HTTPException
from pydantic    import BaseModel,Field
from typing     import List, Optional

fastapi_app = FastAPI(title="Employee CRUD API", description="A simple CRUD API for managing employees", version="1.0.0")

# pydantic model for employee
class Employee(BaseModel):
    id:int =Field(..., description="The unique identifier for the employee")
    name:str = Field(..., max_length=100, min_length=2, description="The name of the employee")
    salary:float =Field(...,gt=0, description="The salary of the employee")
    department:str =Field(...,max_length=50, description="The department of the employee")

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, min_length=2, description="The name of the employee")
    salary: Optional[float] = Field(None, gt=0, description="The salary of the employee")
    department: Optional[str] = Field(None, max_length=50, description="The department of the employee")


employees: List[Employee] = [Employee(id=1, name="John Doe", salary=50000, department="Engineering"),
                             Employee(id=2, name="Jane Smith", salary=60000, department="Marketing")]

@fastapi_app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is healthy"}    

@fastapi_app.get("/employees", response_model=List[Employee], tags=["Employees"])
def get_employees():
    return employees

@fastapi_app.post("/employees", response_model=Employee, tags=["Create Employee"])
def create_employee(newEmployee: Employee):
    for e in employees:
        if e.id == newEmployee.id:
            raise HTTPException(status_code=400, detail=f"Employee with id {e.id} already exists")
    employees.append(newEmployee)
    return newEmployee

@fastapi_app.get("/employees/{id}", response_model=Employee, tags=["getById"])
def get_by_id(id:int):
    for e in employees:
        if(e.id == id):
            return e
    raise HTTPException(status_code=400, detail=f"Id does not exist{id}")

@fastapi_app.delete("/employees/{id}", tags=["deleteById"])
def deleteById(id:int):
    for e in employees:
        if(e.id == id):
            employees.remove(e)
            return {"status": "ok", "message": f"employee with {id} deleted"}
    raise HTTPException(status_code=400, detail=f"employee not found {id}")    

@fastapi_app.put("/employees/{id}", response_model=Employee, tags=["update"])
def updateEmployee(id:int, updatedEmployee: EmployeeUpdate):
    for e in employees:
        if(e.id == id):
            if updatedEmployee.department is not None:
                e.department = updatedEmployee.department
            if updatedEmployee.name is not None:
                e.name = updatedEmployee.name
            if updatedEmployee.salary is not None:
                e.salary = updatedEmployee.salary
            return e 
    raise HTTPException(status_code=400, detail=f"Data not dound for {id}")            

    