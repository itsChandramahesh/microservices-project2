from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .database import Base,engine
from .routes import router
app=FastAPI(title="Order Service")
REQUEST_COUNT=Counter("order_service_requests_total","Order service requests",["path","method"])
@app.on_event("startup")
def startup():Base.metadata.create_all(engine)
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
