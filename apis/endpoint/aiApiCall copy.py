from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiRespose
from openai import OpenAI
import os
from dotenv import load_dotenv
from ultralytics import YOLO

# Load an official or custom model
model = YOLO("yolo11n.pt")  # Load an official Detect model

# 하드코딩 파라미터 (예시)
FOCAL_LENGTH_PX = 800      # 카메라 초점거리 (픽셀)
DISTANCE_CM = 0    

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

@router.post("/call", response_model=aiRespose)
def generate_text(item: userInputParam):
    for result in model.track(0, show=True, tracker="bytetrack.yaml", stream=True):
        boxes = result.boxes  # 감지된 박스들
        if boxes is not None and len(boxes) > 0:
            # 가장 큰 오브젝트 찾기 (가로*세로 픽셀 기준)
            max_box = max(
                boxes,
                key=lambda box: (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])
            )
            x1, y1, x2, y2 = max_box.xyxy[0].tolist()
            width_px = int(x2 - x1)
            height_px = int(y2 - y1)
            print(f"가장 큰 오브젝트 - 가로: {width_px} px, 세로: {height_px} px")

            # ✅ 실제 가로/세로 길이 계산 (Pinhole camera model)
            # 실제 크기 = (픽셀 크기 * 실제 거리) / 초점 거리
            real_width_cm = (width_px * DISTANCE_CM) / FOCAL_LENGTH_PX
            real_height_cm = (height_px * DISTANCE_CM) / FOCAL_LENGTH_PX
            if(DISTANCE_CM > 10):
                userInputParam.width_cm = int(real_width_cm)
                userInputParam.height_cm = int(real_height_cm)
                generate_text1(userInputParam)
                break;
        DISTANCE_CM += 1

def generate_text1(item: userInputParam):
    return generate_plan(item)