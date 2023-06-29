from pydantic import BaseModel
from typing import Text, Dict, Optional

class NextPage(BaseModel):
    url: str

class NextPage_response:
    url: Dict[str, str] = {"url": "string"}
