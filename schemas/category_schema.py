from pydantic import BaseModel
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    