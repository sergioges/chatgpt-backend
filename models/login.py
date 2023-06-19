from pydantic import BaseModel

# login model
class Login(BaseModel):
    email: str
    password: str