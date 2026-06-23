from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .routes import router
from .database import inventory
app=FastAPI(title="Inventory Service")
REQUEST_COUNT=Counter("inventory_service_requests_total","Inventory service requests",["path","method"])
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
@app.on_event("startup")
async def seed():
 for product_id in range(1,11):
  await inventory.update_one({"product_id":product_id},{"$setOnInsert":{"available_stock":100,"reserved_stock":0}},upsert=True)
app.include_router(router)
