from pydantic import BaseModel
from typing import Text, Dict, Optional

# context model
class Context(BaseModel):
    role: Optional[str] = "system"
    content: Text
    background: str

class Context_response(BaseModel):
    image: Dict[str, str] = {"url": "string", "description": "string"}
    user: Dict[str, str] = {"name": "string", "link": "string", "profile_image": "string"}

class Conversation_response(BaseModel):
    role: str = "assistant"
    content: Text
    
class SavedContext(BaseModel):
    role: Optional[str] = "system"
    content: str
    background: str