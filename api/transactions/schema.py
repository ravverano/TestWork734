from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

class CreateTransaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

