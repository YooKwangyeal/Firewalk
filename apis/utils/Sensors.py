import random
from pydantic import BaseModel
from typing import Optional
from ultralytics import YOLO
import math
import cv2

sensors : type = ['니트로글리콜', 'TNT', '테트릴']

# YOLO 모델은 서버 시작 시 1회만 로드
model = YOLO("yolo11n.pt")

class Sensors:
    
    def getExplosiveElementBySors():
        try:
            idx = random.randint(0, 2)
            return sensors[idx]
        
        except ImportError:
            print("sensors module is not available.")

    def getWHByYoloModel():
        try:
            DISTANCE_CM = 50
            NUM_FRAMES = 10

            width_px_list = []
            height_px_list = []
            # OpenCV VideoCapture를 직접 사용하여 웹캠 제어
            video_path = './drone.mp4'
            res = model.track('./drone.mp4', show=True, tracker="bytetrack.yaml", stream=False)
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return 0, 0, 0, "웹캠을 열 수 없습니다."
            
            try:
                frame_count = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # YOLO 모델로 단일 프레임 추론
                    results = model.track(frame, show=False, tracker="bytetrack.yaml", persist=True)
                    
                    if results and len(results) > 0:
                        result = results[0]
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

                            if DISTANCE_CM >= 30:
                                width_px_list.append(width_px)
                                height_px_list.append(height_px)
                                print('len(width_px_list) : ', len(width_px_list))
                                
                                if len(width_px_list) >= NUM_FRAMES:
                                    break
                            DISTANCE_CM += 1
                        else:
                            print(f"[{frame_count+1}] 오브젝트를 감지하지 못했습니다.")
                    
                    frame_count += 1
                    
                    # 너무 많은 프레임을 처리하지 않도록 제한
                    if frame_count > 100:
                        break
                        
            finally:
                # 웹캠 리소스 명시적 해제
                cap.release()
                cv2.destroyAllWindows()
            
            # 충분한 데이터를 수집하지 못한 경우 기본값 사용
            if not width_px_list or not height_px_list:
                width_px = 100  # 기본값
                height_px = 100  # 기본값
            else:
                # 평균값 사용
                width_px = sum(width_px_list) / len(width_px_list)
                height_px = sum(height_px_list) / len(height_px_list)
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
            
            return object_width_m, object_depth_m, object_height_m, "success"
            
        except ImportError:
            return 0, 0, 0, "YoloModel is not available."