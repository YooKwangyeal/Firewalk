from pydantic import BaseModel
from typing import Optional


class userInputParam(BaseModel):
    prompt:  Optional[str]
    max_length: Optional[int] = 50
    image : Optional[str] = None


class aiRespose(BaseModel):
    response: str
    action: str