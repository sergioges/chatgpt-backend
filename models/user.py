from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# user model
class User(BaseModel):
    id:  Optional[str]
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    registration: str

class UserEdit(BaseModel):
    id:  Optional[str]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    active: Optional[bool] = True
    registration: Optional[str]