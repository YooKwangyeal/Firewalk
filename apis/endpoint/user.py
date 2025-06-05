from fastapi import APIRouter
from pydantic import BaseModel
from database import engineconn
from apis.model import userModel 


router = APIRouter()

engine = engineconn()
session = engine.sessionmaker()

@router.post("/info")
def selectUserInfo(params : userModel.userSelectParam):
    user_info = session.query(userModel.User).filter(userModel.User.u_id == params.m_id).first()
    return user_info

@router.post("/insertUser")
def insert(params : userModel.userPutParam):
    print("앱에서 받은 데이터:", params.dict())  # 추가
    new_user = userModel.User(
        m_sns_key=params.m_sns_key,
        m_relate_type=params.m_relate_type,
        nickname=params.nickname,
        email=params.email
    )
    session.add(new_user)
    session.commit()    
    userNo = new_user.u_no
    session.close()
    return {"userNo": userNo}