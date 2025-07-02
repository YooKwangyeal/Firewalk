from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 추가
from apis.router import api_router


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, reload=True)