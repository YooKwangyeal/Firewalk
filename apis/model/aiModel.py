from pydantic import BaseModel
from typing import Optional


class userInputParam(BaseModel):
    explosive_type: Optional[str] = "C4"
    width_cm: Optional[int] = 50
    height_cm: Optional[int] = 30
    depth_cm: Optional[int] = 20
    temperature: Optional[float] = 0.7
    max_length: Optional[int] = 50
    image: Optional[str] = None

    @property
    def prompt(self) -> str:
        return (
            f"당신은 폭발 피해 평가 전문가입니다.\n\n"
            f"의심스러운 물체가 발견되었으며, {self.explosive_type}가 포함되어 있을 것으로 추정됩니다.\n"
            f"해당 물체의 예상 크기는 다음과 같습니다:\n"
            f"- 가로: {self.width_cm} cm\n"
            f"- 세로: {self.height_cm} cm\n"
            f"- 높이: {self.depth_cm} cm\n\n"
            f"아래 내용을 반드시 한국어로 작성해 주세요. 영어로 답변하지 마세요.\n"
            f"1. 이 물체에 고성능 {self.explosive_type} 폭약이 들어있을 경우 예상 폭발 반경을 추정해 주세요.\n"
            f"2. 안전 수칙 및 권장 대피 반경을 안내해 주세요.\n"
            f"3. 위 내용을 한국어로 간결하게 요약 보고서(불릿포인트)로 작성해 주세요."
        )


class aiRespose(BaseModel):
    response: str
    action: str