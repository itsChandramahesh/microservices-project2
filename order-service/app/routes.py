from decimal import Decimal
import httpx
from fastapi import APIRouter,Depends,HTTPException,Header
from sqlalchemy.orm import Session
from sqlalchemy import func,select
from .config import settings
from .database import get_db
from .models import Order,OrderItem
from .schemas import OrderOut,Status
from .auth import claims,admin
from .crud import user_orders
router=APIRouter()
@router.post("/",response_model=OrderOut,status_code=201)
async def create(authorization:str=Header(...),c=Depends(claims),db:Session=Depends(get_db)):
 async with httpx.AsyncClient(timeout=10) as client:
  cart=(await client.get(settings.cart_url,headers={"Authorization":authorization})).json()
  if not cart.get("items"):raise HTTPException(400,"Cart is empty")
  rows=[];total=Decimal(0)
  for item in cart["items"]:
   product=(await client.get(f"{settings.product_url}/{item['product_id']}")).json()
   response=await client.post(f"{settings.inventory_url}/{item['product_id']}/reserve",json={"quantity":item["quantity"]})
   if response.status_code>=400:raise HTTPException(409,f"Cannot reserve product {item['product_id']}")
   price=Decimal(str(product["price"]));rows.append(OrderItem(product_id=item["product_id"],quantity=item["quantity"],unit_price=price));total+=price*item["quantity"]
  order=Order(user_id=c["sub"],total=total,items=rows);db.add(order);db.commit();db.refresh(order)
  await client.delete(settings.cart_url,headers={"Authorization":authorization})
  return order
@router.get("/",response_model=list[OrderOut])
def list_orders(c=Depends(claims),db:Session=Depends(get_db)):return user_orders(db,c["sub"])
@router.get("/admin/stats",dependencies=[Depends(admin)])
def stats(db:Session=Depends(get_db)):return {"total_orders":db.scalar(select(func.count(Order.id))) or 0}
@router.get("/{order_id}",response_model=OrderOut)
def get(order_id:int,c=Depends(claims),db:Session=Depends(get_db)):
 obj=db.get(Order,order_id)
 if not obj or (obj.user_id!=c["sub"] and c.get("role")!="ADMIN"):raise HTTPException(404,"Order not found")
 return obj
@router.put("/{order_id}/status",response_model=OrderOut,dependencies=[Depends(admin)])
def status(order_id:int,data:Status,db:Session=Depends(get_db)):
 obj=db.get(Order,order_id)
 if not obj:raise HTTPException(404,"Order not found")
 obj.status=data.status;db.commit();db.refresh(obj);return obj
