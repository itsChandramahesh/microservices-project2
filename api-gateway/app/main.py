import httpx
from fastapi import FastAPI,Request,Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from .config import settings
app=FastAPI(title="E-Commerce API Gateway")
targets={"users":settings.user_service_url,"products":settings.product_service_url,"cart":settings.cart_service_url,"inventory":settings.inventory_service_url,"orders":settings.order_service_url,"payments":settings.payment_service_url,"admin":settings.admin_service_url}
REQUEST_COUNT=Counter("api_gateway_requests_total","API gateway requests",["path","method"])
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
@app.api_route("/api/{service}/{path:path}",methods=["GET","POST","PUT","PATCH","DELETE"])
async def proxy(service:str,path:str,request:Request):
 if service not in targets:return Response("Unknown service",status_code=404)
 url=f"{targets[service]}/{path}" if path else targets[service]
 async with httpx.AsyncClient(timeout=30) as client:
  response=await client.request(request.method,url,params=request.query_params,content=await request.body(),headers={k:v for k,v in request.headers.items() if k.lower() not in {"host","content-length"}})
 return Response(response.content,status_code=response.status_code,headers={k:v for k,v in response.headers.items() if k.lower() not in {"content-length","content-encoding","transfer-encoding"}})
