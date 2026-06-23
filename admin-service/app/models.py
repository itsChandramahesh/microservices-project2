from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class Category(Base):
 __tablename__="categories";id:Mapped[int]=mapped_column(primary_key=True);name:Mapped[str]=mapped_column(String(100),unique=True);description:Mapped[str]=mapped_column(String(500),default="")

