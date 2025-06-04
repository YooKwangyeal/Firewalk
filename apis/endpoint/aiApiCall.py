from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiRespose
from openai import OpenAI
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_plan(item: userInputParam) -> aiRespose:
    prompt = item.prompt
    max_length = item.max_length

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 필요시 gpt-4로 변경
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_length
        )
        result = response.choices[0].message.content
        return aiRespose(response=result, action="")
    except Exception as e:
        return aiRespose(response="Error occurred", action=str(e))

@router.post("/generate", response_model=aiRespose)
def generate_text(item: userInputParam):
    return generate_plan(item)