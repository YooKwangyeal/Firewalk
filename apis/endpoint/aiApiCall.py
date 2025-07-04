from fastapi import APIRouter
from apis.model.aiModel import userInputParam, aiResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from apis.utils.parser import parse_ai_response
from apis.utils.Sensors import Sensors

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

def generate_plan(item: userInputParam) -> aiResponse:
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
        return aiResponse(response=result, action="")
    except Exception as e:
        return aiResponse(response="Error occurred", action=str(e))

@router.post("/generate", response_model=aiResponse)
def generate_text(item: userInputParam):
    return generate_plan(item)

# --- YOLO 실시간 감지 API ---
@router.post("/detect")
def detect_object(item: userInputParam):
    FOCAL_LENGTH_PX = 800      # 카메라 초점거리 (픽셀)
    DISTANCE_CM = 30           # 카메라와 오브젝트 사이 거리 (cm, 예시)
    NUM_FRAMES = 10

    width_px_list = []
    height_px_list = []

    # 10프레임 동안 반복
    for idx, result in enumerate(model.track(0, show=False, tracker="bytetrack.yaml", stream=True)):
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
            width_px_list.append(width_px)
            height_px_list.append(height_px)
            print(f"[{idx+1}] Detected object: width_px={width_px}, height_px={height_px}")

            if len(width_px_list) >= NUM_FRAMES:
                break
        else:
            print(f"[{idx+1}] 오브젝트를 감지하지 못했습니다.")

    if len(width_px_list) == 0:
        return {"error": "오브젝트를 감지하지 못했습니다."}

    # 10프레임 평균
    avg_width_px = sum(width_px_list) / len(width_px_list)
    avg_height_px = sum(height_px_list) / len(height_px_list)

    # 실제 가로/세로 길이 계산
    real_width_cm = (avg_width_px * DISTANCE_CM) / FOCAL_LENGTH_PX
    real_height_cm = (avg_height_px * DISTANCE_CM) / FOCAL_LENGTH_PX

    # item에 값 할당
    item.width_cm = real_width_cm
    item.height_cm = real_height_cm
    item.depth_cm = DISTANCE_CM

    prompt = item.prompt
    max_length = item.max_length
    print(prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_length
        )
        result = response.choices[0].message.content
        parsed = parse_ai_response(result)
        return parsed
    except Exception as e:
        return aiResponse(response="Error occurred", action=str(e))
        DISTANCE_CM += 1


@router.post("/test", response_model=aiResponse)
def generate_test(item: userInputParam):

    explosive_type = Sensors.getExplosiveElementBySors()

    width , height, depth ,msg = Sensors.getWHByYoloModel()

    item.explosive_type = explosive_type
    item.width_cm = width
    item.height_cm = height
    item.depth_cm = depth
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
        parsed = parse_ai_response(result)
        return parsed
    except Exception as e:
        return aiResponse(response="Error occurred", action=str(e))
