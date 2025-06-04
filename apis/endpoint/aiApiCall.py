from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiRespose
from apis.service import gpt_service  # ✅ GPT 기능만 import

router = APIRouter()

@router.post("/generate", response_model=aiRespose)
def generate_text(item: userInputParam):
    return gpt_service.generate_plan(item)  # ✅ gpt_service의 generate_plan만 호출