from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Order,OrderItem
def user_orders(db:Session,user_id:str):return list(db.scalars(select(Order).where(Order.user_id==user_id).order_by(Order.id.desc())))

