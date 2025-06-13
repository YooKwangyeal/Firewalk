from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()
TOUR_API_KEY = os.getenv("TOUR_API_KEY")

class TourRequest(BaseModel):
    """
    실제 API 요청에 사용되는 파라미터 모델입니다.
    """
    numOfRows: int = 10  # 한 페이지 결과 수 (기본값: 10)
    pageNo: int = 1  # 페이지 번호 (기본값: 1)
    MobileOS: str = 'AND'  # OS 구분 (IOS, AND, WEB, ETC)
    MobileApp: str = 'gochunsick'  # 서비스명(어플명)
    type_: str = Field('json', alias='_type')  # 응답 메시지 형식 (json, 기본값)
    arrange: str = 'A'  # 정렬구분 (A=제목순, C=수정일순, D=생성일순 등)
    contentTypeId: Optional[str] = None  # 관광타입 ID (12:관광지, 14:문화시설 등)
    areaCode: Optional[str] = None  # 관광지 지역 코드
    sigunguCode: Optional[str] = None  # 관광지 시군구 코드
    cat1: Optional[str] = None  # 대분류 코드
    cat2: Optional[str] = None  # 중분류 코드
    cat3: Optional[str] = None  # 소분류 코드
    modifiedtime: Optional[str] = None  # 수정일 (형식: YYYYMMDD)
    serviceKey: str = TOUR_API_KEY  # 서비스 인증키 (필수)
    lDongRegnCd: Optional[str] = None  # 법정동 시도 코드
    lDongSignguCd: Optional[str] = None  # 법정동 시군구 코드
    lclsSystm1: Optional[str] = None  # 분류체계 대분류
    lclsSystm2: Optional[str] = None  # 분류체계 중분류
    lclsSystm3: Optional[str] = None  # 분류체계 소분류

class TourItem(BaseModel):
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    areacode: Optional[str] = None
    cat1: Optional[str] = None
    cat2: Optional[str] = None
    cat3: Optional[str] = None
    contentid: Optional[str] = None
    contenttypeid: Optional[str] = None
    createdtime: Optional[str] = None
    firstimage: Optional[str] = None
    firstimage2: Optional[str] = None
    cpyrhtDivCd: Optional[str] = None
    mapx: Optional[float] = None
    mapy: Optional[float] = None
    mlevel: Optional[int] = None
    modifiedtime: Optional[str] = None
    sigungucode: Optional[str] = None
    tel: Optional[str] = None
    title: Optional[str] = None
    zipcode: Optional[str] = None
    lDongRegnCd: Optional[str] = None
    lDongSignguCd: Optional[str] = None
    lclsSystm1: Optional[str] = None
    lclsSystm2: Optional[str] = None
    lclsSystm3: Optional[str] = None

class Items(BaseModel):
    item: List[TourItem]

class TourResponseBody(BaseModel):
    items: Items
    numOfRows: Optional[int]
    pageNo: Optional[int]
    totalCount: Optional[int]

class TourResponseHeader(BaseModel):
    resultCode: str
    resultMsg: str

class TourResponseResponse(BaseModel):
    header: TourResponseHeader
    body: TourResponseBody

class TourResponse(BaseModel):
    response: TourResponseResponse