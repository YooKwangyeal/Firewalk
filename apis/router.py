from fastapi import APIRouter
from apis.endpoint import aiApiCall

api_router = APIRouter()

api_router.include_router(aiApiCall.router, prefix="/ai", tags=["aiApiCall"])