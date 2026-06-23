import os
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .database import Base,engine,SessionLocal
from .models import User
from .routes import router
from .crud import create,by_email
from .schemas import Register
app=FastAPI(title="User Service")
REQUEST_COUNT=Counter("user_service_requests_total","User service requests",["path","method"])
@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        email=os.getenv("ADMIN_EMAIL","admin@example.com")
        if not by_email(db,email): create(db,Register(email=email,name="Administrator",password=os.getenv("ADMIN_PASSWORD","Admin123!")),"ADMIN")
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(path=request.url.path, method=request.method).inc()
    return response
app.include_router(router)
