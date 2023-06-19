from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime

# context model
class Question(BaseModel):
    role: str = "user"
    content: Text

class QuestionEdit(BaseModel):
    question_id: str
    role: Optional[str]
    content: Text
    registration: Optional[datetime]