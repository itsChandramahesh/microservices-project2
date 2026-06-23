from fastapi import APIRouter,Depends,HTTPException,Header
import httpx
from .config import settings
from sqlalchemy import select
from sqlalchemy.orm import Session
from .auth import admin
from .database import get_db
from .models import Category
from .schemas import CategoryIn,CategoryOut
from .crud import create
router=APIRouter(dependencies=[Depends(admin)])
@router.get("/dashboard")
async def dashboard(authorization:str=Header(...)):
 headers={"Authorization":authorization};urls=[settings.user_service_url+"/admin/stats",settings.product_service_url+"/admin/stats",settings.order_service_url+"/admin/stats",settings.payment_service_url+"/admin/stats"]
 async with httpx.AsyncClient(timeout=10) as client:responses=await __import__("asyncio").gather(*(client.get(url,headers=headers) for url in urls))
 result={}
 for response in responses:
  if response.status_code>=400:raise HTTPException(502,"Analytics dependency unavailable")
  result.update(response.json())
 return result
@router.get("/categories",response_model=list[CategoryOut])
def categories(db:Session=Depends(get_db)):return list(db.scalars(select(Category)))
@router.post("/categories",response_model=CategoryOut,status_code=201)
def add(data:CategoryIn,db:Session=Depends(get_db)):return create(db,data)
@router.put("/categories/{category_id}",response_model=CategoryOut)
def edit(category_id:int,data:CategoryIn,db:Session=Depends(get_db)):
 obj=db.get(Category,category_id)
 if not obj:raise HTTPException(404,"Category not found")
 obj.name=data.name;obj.description=data.description;db.commit();db.refresh(obj);return obj
@router.delete("/categories/{category_id}",status_code=204)
def delete(category_id:int,db:Session=Depends(get_db)):
 obj=db.get(Category,category_id)
 if not obj:raise HTTPException(404,"Category not found")
 db.delete(obj);db.commit()
