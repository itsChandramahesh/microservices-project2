from decimal import Decimal
from sqlalchemy import String,Text,Numeric,Integer
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class Product(Base):
    __tablename__="products"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200),index=True)
    description:Mapped[str]=mapped_column(Text,default="")
    price:Mapped[Decimal]=mapped_column(Numeric(12,2))
    stock:Mapped[int]=mapped_column(Integer,default=0)
    category:Mapped[str]=mapped_column(String(100),index=True)
    image_url:Mapped[str|None]=mapped_column(String(500),nullable=True)

