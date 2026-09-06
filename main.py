from fastapi    import FastAPI, HTTPException, status
from typing     import List, Optional
from models.employee import Employee, EmployeeUpdate
from database.employeerepo import employees
from models.base_model import base_response
from fastapi.responses import JSONResponse

fastapi_app = FastAPI(title="Employee CRUD API", description="A simple CRUD API for managing employees", version="1.0.0")

# pydantic model for employee



@fastapi_app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is healthy"}    

# @fastapi_app.get("/employees", response_model=List[Employee], tags=["Employees"])
@fastapi_app.get("/employees", response_model=base_response, tags=["Employees"])
def get_employees():
    
    response = base_response(code=status.HTTP_200_OK,status=str(status.HTTP_200_OK), data=employees, message=str(status.HTTP_200_OK))
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump()
     )
    # return response

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

    