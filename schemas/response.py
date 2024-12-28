from typing import Any, Literal, Optional
from pydantic import BaseModel

# response schemas
class GetResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    data: Optional[Any] = []