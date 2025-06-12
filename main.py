from fastapi import FastAPI
from apis.router import api_router


app = FastAPI(
    title="FastAPI Example",
    description="A simple FastAPI example",
    version="1.0.0",
    docs_url="/docs"
)


app.include_router(api_router, prefix="/api", tags=["api"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, reload=True)