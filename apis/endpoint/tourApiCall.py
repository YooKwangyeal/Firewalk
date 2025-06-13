from fastapi import APIRouter
from apis.model.tourModel import TourRequest, TourResponse
import requests
import certifi

router = APIRouter()

TOUR_API_URL = "http://apis.data.go.kr/B551011/KorService2/areaBasedList2"

@router.post("/tour", response_model=TourResponse)
def get_tour_list(params: TourRequest):
    """
    Tour API(지역기반관광정보조회) 호출 예시
    """
    # None 값과 "string" 값은 제외
    query = {k: v for k, v in params.model_dump(by_alias=True, exclude_none=True).items() if v != "string"}
    res = requests.get(TOUR_API_URL, params=query, verify=certifi.where())
    data = res.json()
    return TourResponse(**data)