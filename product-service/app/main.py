from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .database import Base,engine,SessionLocal
from .models import Product
from .schemas import ProductCreate
from .crud import create
from .routes import router
app=FastAPI(title="Product Service")
REQUEST_COUNT=Counter("product_service_requests_total","Product service requests",["path","method"])
@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(Product).count()==0:
            for i in range(1,11):create(db,ProductCreate(name=f"Product {i}",description=f"Seed product {i}",price=10*i,stock=100,category=f"Category {(i-1)%5+1}"))
@app.get("/health")
def health():return {"status":"ok"}
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(path=request.url.path, method=request.method).inc()
    return response
app.include_router(router)
