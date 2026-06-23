from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func,select
from .database import get_db
from .schemas import PaymentCreate,PaymentOut
from .models import Payment
from .crud import create
from .auth import claims
router=APIRouter()
@router.post("/",response_model=PaymentOut,status_code=201)
def pay(data:PaymentCreate,c=Depends(claims),db:Session=Depends(get_db)):return create(db,data,c["sub"])
@router.get("/admin/stats")
def stats(c=Depends(claims),db:Session=Depends(get_db)):
 if c.get("role")!="ADMIN":raise HTTPException(403,"Admin role required")
 total=db.scalar(select(func.count(Payment.id))) or 0
 revenue=db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.status=="SUCCESS")) or 0
 return {"total_payments":total,"revenue":revenue}
@router.get("/{payment_id}",response_model=PaymentOut)
def get(payment_id:int,c=Depends(claims),db:Session=Depends(get_db)):
 obj=db.get(Payment,payment_id)
 if not obj or (obj.user_id!=c["sub"] and c.get("role")!="ADMIN"):raise HTTPException(404,"Payment not found")
 return obj
