from pydantic import BaseModel
from typing import Optional

# user model
class User(BaseModel):
    id:  Optional[str]
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    registration: Optional[str]