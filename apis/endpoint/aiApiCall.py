from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiRespose
from openai import OpenAI
import os
from dotenv import load_dotenv

# YOLO import 및 모델 로드
from ultralytics import YOLO

router = APIRouter()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# YOLO 모델은 서버 시작 시 1회만 로드
model = YOLO("yolo11n.pt")

# 하드코딩 파라미터 (예시)
FOCAL_LENGTH_PX = 800      # 카메라 초점거리 (픽셀)


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

# --- YOLO 실시간 감지 API ---
@router.post("/detect")
def detect_object(item: userInputParam):
    """
    웹캠에서 한 프레임을 감지하여 가장 큰 오브젝트의 픽셀/실제 크기를 반환
    """
    DISTANCE_CM = 10          # 카메라와 오브젝트 사이 거리 (cm, 예시)
    # 웹캠에서 한 프레임만 추론 (stream=True 사용)
    for result in model.track(0, show=True, tracker="bytetrack.yaml", stream=True):
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            # 가장 큰 오브젝트 찾기
            max_box = max(
                boxes,
                key=lambda box: (box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1])
            )
            x1, y1, x2, y2 = max_box.xyxy[0].tolist()
            width_px = int(x2 - x1)
            height_px = int(y2 - y1)
            print(f"Detected object at: x1={x1}, y1={y1}, x2={x2}, y2={y2}, width_px={width_px}, height_px={height_px}")

            if(DISTANCE_CM > 100) : 
                # 실제 가로/세로 길이 계산
                real_width_cm = (width_px * DISTANCE_CM) / FOCAL_LENGTH_PX
                real_height_cm = (height_px * DISTANCE_CM) / FOCAL_LENGTH_PX
                item.width_cm = real_width_cm
                item.height_cm = real_height_cm
                prompt = item.prompt
                max_length = item.max_length
                print(prompt)
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
        else:
            return {"error": "오브젝트를 감지하지 못했습니다."}
        DISTANCE_CM += 1