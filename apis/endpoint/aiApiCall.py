from fastapi import APIRouter
from apis.model import aiModel

router = APIRouter()

@router.post("/info")
def selectUserInfo():
    
    return ""