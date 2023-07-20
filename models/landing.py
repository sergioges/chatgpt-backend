from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# user model
class Register(BaseModel):
    id: Optional[str]
    email: str
    registration: Optional[datetime]