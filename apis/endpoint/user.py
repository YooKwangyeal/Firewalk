from fastapi import APIRouter
from pydantic import BaseModel
from database import engineconn
from apis.model import userModel 


router = APIRouter()

engine = engineconn()
session = engine.sessionmaker()

@router.post("/info")
def selectUserInfo(params : userModel.userSelectParam):
    user_info = session.query(userModel.User).filter(userModel.User.m_id == params.m_id).first()
    return user_info

@router.post("/insertUser")
def insert(params : userModel.userPutParam):
    print("앱에서 받은 데이터:", params.dict())
    new_user = userModel.User(
        nickname=params.nickname,
        email=params.email,
        m_gender=params.m_gender,
        m_sns_key=params.m_sns_key,
        m_sns_type=params.m_sns_type,
    )
    session.add(new_user)
    session.commit()    
    userNo = new_user.u_no
    session.close()
    return {"userNo": userNo}