from datetime import datetime
from decimal import Decimal
from sqlalchemy import String,Numeric,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class Payment(Base):
 __tablename__="payments";id:Mapped[int]=mapped_column(primary_key=True);order_id:Mapped[int]=mapped_column(index=True);user_id:Mapped[str]=mapped_column(String(64));amount:Mapped[Decimal]=mapped_column(Numeric(12,2));status:Mapped[str]=mapped_column(String(20));created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())

