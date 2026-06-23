from sqlalchemy.orm import Session
from .models import Payment
def create(db:Session,data,user_id):
 obj=Payment(order_id=data.order_id,amount=data.amount,user_id=user_id,status="SUCCESS" if data.succeed else "FAILED");db.add(obj);db.commit();db.refresh(obj);return obj

