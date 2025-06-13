from fastapi import APIRouter
from apis.endpoint import user, aiApiCall, tourApiCall

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(aiApiCall.router, prefix="/ai", tags=["aiApiCall"])
api_router.include_router(tourApiCall.router, prefix="/tour", tags=["tourApiCall"])