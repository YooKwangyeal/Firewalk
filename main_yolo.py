from ultralytics import YOLO

# Load an official or custom model
model = YOLO("yolo11n.pt")  # Load an official Detect model

# 하드코딩 파라미터 (예시)
FOCAL_LENGTH_PX = 800      # 카메라 초점거리 (픽셀)
DISTANCE_CM = 100          # 카메라와 오브젝트 사이 거리 (cm, 예시)

# 웹캠에서 프레임 추출 및 추론
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

        print(f"실제 가로 길이: {real_width_cm:.2f} cm")
        print(f"실제 세로 길이: {real_height_cm:.2f} cm")