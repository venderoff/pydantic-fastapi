from pydantic import BaseModel,Field

class base_response(BaseModel):
    code: int=Field(..., gt=0)
    status: str=Field(..., min_length=2, max_length=50)
    message: str=Field(..., min_length=2, max_length=50)
    data: object