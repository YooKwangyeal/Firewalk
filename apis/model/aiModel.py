from pydantic import BaseModel
from typing import Optional


class userInputParam(BaseModel):
    prompt:  Optional[str] = "Generate a plan for a trip to Jeju Island"
    temperature: Optional[float] = 0.7
    max_length: Optional[int] = 50
    image : Optional[str] = None


class aiRespose(BaseModel):
    response: str
    action: str