from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 추가
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from apis.router import api_router
import os


app = FastAPI(
    title="FastAPI Example",
    description="A simple FastAPI example",
    version="1.0.0",
    docs_url="/docs"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 * 사용, 운영 시에는 실제 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api", tags=["api"])

# 정적 파일 마운트 (CSS, JS, 이미지 등)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 루트 경로에서 index.html 서빙
@app.get("/")
async def read_index():
    return FileResponse('frontend/explosive_form.html')

# frontend 폴더의 HTML 파일들을 직접 접근할 수 있도록 설정
@app.get("/explosive_form")
async def explosive_form():
    return FileResponse('frontend/explosive_form.html')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, reload=True)