from datetime import datetime
from decimal import Decimal
from sqlalchemy import String,DateTime,Numeric,ForeignKey,Integer,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .database import Base
class Order(Base):
 __tablename__="orders";id:Mapped[int]=mapped_column(primary_key=True);user_id:Mapped[str]=mapped_column(String(64),index=True);status:Mapped[str]=mapped_column(String(30),default="PENDING");total:Mapped[Decimal]=mapped_column(Numeric(12,2));created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now());items:Mapped[list["OrderItem"]]=relationship(cascade="all, delete-orphan",lazy="selectin")
class OrderItem(Base):
 __tablename__="order_items";id:Mapped[int]=mapped_column(primary_key=True);order_id:Mapped[int]=mapped_column(ForeignKey("orders.id"));product_id:Mapped[int]=mapped_column(Integer);quantity:Mapped[int]=mapped_column(Integer);unit_price:Mapped[Decimal]=mapped_column(Numeric(12,2))

