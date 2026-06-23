from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .database import Base,engine,SessionLocal
from .models import Category
from .routes import router
app=FastAPI(title="Admin Service")
REQUEST_COUNT=Counter("admin_service_requests_total","Admin service requests",["path","method"])
@app.on_event("startup")
def startup():
 Base.metadata.create_all(engine)
 with SessionLocal() as db:
  if db.query(Category).count()==0:db.add_all([Category(name=f"Category {i}") for i in range(1,6)]);db.commit()
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/metrics")
def metrics():
 return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.middleware("http")
async def metrics_middleware(request, call_next):
 response=await call_next(request)
 REQUEST_COUNT.labels(path=request.url.path, method=request.method).inc()
 return response
app.include_router(router)
