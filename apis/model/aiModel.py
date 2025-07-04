from pydantic import BaseModel
from typing import Optional, List


class userInputParam(BaseModel):
    explosive_type: Optional[str] = "C4"
    width_cm: Optional[int] = 0
    height_cm: Optional[int] = 0
    depth_cm: Optional[int] = 20
    temperature: Optional[float] = 0.7
    max_length: Optional[int] = 300
    image: Optional[str] = None

    @property
    def base_prompt(self) -> str:
        return (
            "당신은 폭발 피해 평가 전문가입니다.\n\n"
            "사용자로부터 폭발물이 의심되는 객체 정보가 주어졌습니다.\n"
            "아래 입력값을 바탕으로 예상 피해 범위 및 대응 가이드를 작성해 주세요.\n"
            "현재 폭발 위치는 서울역으로 가정합니다.\n"
            "다음 형식에 맞춰 반드시 한국어로만 답변하세요:\n"
            "폭발 반경: [숫자] 미터\n"
            "대피 반경: [숫자] 미터\n"
            "위험 좌표: [위도, 경도]\n"
            "요약:\n"
            "- (불릿포인트 요약)\n"
            "다음은 사용자로부터 전달받은 입력값입니다:\n"
        )

    @property
    def dynamic_prompt(self) -> str:
        return (
            f"- 폭발물 유형: {self.explosive_type}\n"
            f"- 가로 길이: {self.width_cm} cm\n"
            f"- 세로 길이: {self.height_cm} cm\n"
            f"- 높이 (두께): {self.depth_cm} cm\n"
        )

    @property
    def prompt(self) -> str:
        return self.base_prompt + self.dynamic_prompt

# 2. AI 응답 정의
class aiResponse(BaseModel):
    response: str
    blast_radius_m: Optional[int] = None
    evacuation_radius_m: Optional[int] = None
    danger_zone_coords: Optional[list] = None
    summary: Optional[str] = None