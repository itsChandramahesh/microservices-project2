from fastapi import FastAPI

from .database import redis
from .routes import router

app = FastAPI(title="Cart Service")


@app.on_event("startup")
async def startup():
    await redis.ping()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
