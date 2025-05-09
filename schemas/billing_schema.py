from pydantic import BaseModel
from typing import Optional

class BillingBase(BaseModel):
    remarks: Optional[str]
    user_id: str
    category_id: str