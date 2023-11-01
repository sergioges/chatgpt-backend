from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime

# question model
class Question(BaseModel):
    role: str = "user"
    content: Text
    update: Optional[bool]

class QuestionEdit(BaseModel):
    question_id: str
    role: Optional[str]
    content: Text
    registration: Optional[datetime]
    update: Optional[bool]

class QuestionImprove(BaseModel):
    question_id: str
    content: Text
    language: str
    registration: Optional[datetime]
    update: Optional[bool]