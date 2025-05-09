from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BillingBase(BaseModel):
    remarks: Optional[str]
    user_id: int
    category_id: int
    billing_date: datetime
    amount: float