from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiRespose
import openai
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan(item: userInputParam) -> aiRespose:
    prompt = item.prompt
    max_length = item.max_length

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 필요시 gpt-4로 변경
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response["choices"][0]["message"]["content"]
        return aiRespose(response=result, action="")
    except Exception as e:
        return aiRespose(response="Error occurred", action=str(e))

@router.post("/generate", response_model=aiRespose)
def generate_text(item: userInputParam):
    return generate_plan(item)