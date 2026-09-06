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

# @fastapi_app.post("/employees", response_model=Employee, tags=["Create Employee"])
@fastapi_app.post("/employees", response_model=base_response, tags=["Create Employee"])
def create_employee(newEmployee: Employee):
    for e in employees:
        if e.id == newEmployee.id:
            raise HTTPException(status_code=400, detail=f"Employee with id {e.id} already exists")
    employees.append(newEmployee)

    responce = base_response(code=status.HTTP_200_OK, status=str(status.HTTP_200_OK), data=newEmployee, message="successful addition" )

    return JSONResponse(
        status_code=responce.code,
        content=responce.model_dump()
    )

@fastapi_app.get("/employees/{id}", response_model=base_response, tags=["getById"])
def get_by_id(id:int):
    for e in employees:
        if(e.id == id):
            response= base_response(code=status.HTTP_200_OK, data=e, message="success", status=str(status.HTTP_200_OK))
            return JSONResponse(status_code=response.code, content=response.model_dump())
    response= base_response(code=status.HTTP_400_BAD_REQUEST,  message=f"Id does not exist{id}", status=str(status.HTTP_400_BAD_REQUEST), data="")    
    return JSONResponse(status_code=response.code, content=response.model_dump())

@fastapi_app.delete("/employees/{id}", tags=["deleteById"], response_model=base_response)
def deleteById(id:int):
    for e in employees:
        if(e.id == id):
            employees.remove(e)
            response=base_response(status=str(status.HTTP_200_OK), data=e, message="deleted successfully", code=status.HTTP_200_OK)
            return JSONResponse(content=response.model_dump(), status_code=response.code)   
            # return {"status": "ok", "message": f"employee with {id} deleted"}
    response=base_response(status=str(status.HTTP_400_BAD_REQUEST), data="", message=f"id= {id} not available", code=status.HTTP_400_BAD_REQUEST)        
    return JSONResponse(content=response.model_dump(), status_code=response.code)    

@fastapi_app.put("/employees/{id}", response_model=base_response, tags=["update"])
def updateEmployee(id:int, updatedEmployee: EmployeeUpdate):
    for e in employees:
        if(e.id == id):
            if updatedEmployee.department is not None:
                e.department = updatedEmployee.department
            if updatedEmployee.name is not None:
                e.name = updatedEmployee.name
            if updatedEmployee.salary is not None:
                e.salary = updatedEmployee.salary
            response=base_response(status=str(status.HTTP_200_OK), data=e, message="updated successfully", code=status.HTTP_200_OK)
            return JSONResponse(content=response.model_dump(), status_code=response.code) 
    response=base_response(status=str(status.HTTP_400_BAD_REQUEST), data="", message="id = {id} not found", code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content=response.model_dump(), status_code=response.code)
    