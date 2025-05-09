from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str 
    password: str 
    budget: Optional[float]

    
