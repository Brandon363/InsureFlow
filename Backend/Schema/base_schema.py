from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    field: str
    message: str


class BaseResponse(BaseModel):
    status_code: int
    success: bool
    message: str
    errors: Optional[List[ErrorDetail]] | dict = None
