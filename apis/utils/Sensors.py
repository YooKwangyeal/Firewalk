import random
from pydantic import BaseModel
from typing import Optional
from ultralytics import YOLO
import math
import cv2

sensors : type = ['RDX', '니트로글리콜', 'TNT', '테트릴']

# YOLO 모델은 서버 시작 시 1회만 로드
model = YOLO("yolo11n.pt")

# YOLO 모델을 사용하여 폭발물의 크기를 측정하는 클래스
class yoloReturn(BaseModel):
    width: Optional[float] = 0.0
    height: Optional[float] = 0.0
    depth: Optional[float] = 0.0
    msg: Optional[str] = None

class Sensors:
    
    def getExplosiveElementBySors():
        try:
            idx = random.randint(0, 3)
            return sensors[idx]
        
        except ImportError:
            print("sensors module is not available.")

    def getWHByYoloModel():
        result = yoloReturn()
        try:
            # 하드코딩 파라미터 (예시)
            DISTANCE_CM = 0
            NUM_FRAMES = 30

            width_px_list = []
            height_px_list = []

            # 웹캠에서 한 프레임만 추론 (stream=True 사용)
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


                    if(NUM_FRAMES > 30) :
                        width_px_list.append(width_px)
                        height_px_list.append(height_px)
                        if len(width_px_list) >= NUM_FRAMES:
                            break

                else:
                    print(f"[{idx+1}] 오브젝트를 감지하지 못했습니다.")
            # 입력값
            tilt_deg = 60                      # 카메라 틸트 각도
            fov_x_deg = 90                     # 수평 화각
            fov_y_deg = 60                     # 수직 화각
            img_width_px = 1920               # 영상 해상도 (가로)
            img_height_px = 1080              # 영상 해상도 (세로)

            # 장면 가로/세로 폭 계산
            scene_width = 2 * DISTANCE_CM * math.tan(math.radians(fov_x_deg / 2))
            scene_height = 2 * DISTANCE_CM * math.tan(math.radians(fov_y_deg / 2))

            # 픽셀당 크기
            meter_per_px_x = scene_width / img_width_px
            meter_per_px_y = scene_height / img_height_px

            # 가로 & 세로 길이 계산
            object_width_m = width_px * meter_per_px_x
            object_depth_m = height_px * meter_per_px_y  # 이건 화면 상 깊이 방향

            # 높이 계산: 기울어진 화면에서의 세로 방향을 지면 기준 세로로 보정
            # 즉, 깊이 방향 → 수직 높이 보정 (틸트 각도 이용)
            object_height_m = object_depth_m * math.sin(math.radians(tilt_deg))
            result.width = object_width_m
            result.height = object_depth_m
            result.depth = object_height_m
            result.msg = "success"
            
            return result
            
        except ImportError:
            result.width = 0
            result.height = 0
            result.depth = 0
            result.msg = "YoloModel is not available."
            return result

    
