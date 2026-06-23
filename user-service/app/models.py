from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
class Role(str,Enum): USER="USER"; ADMIN="ADMIN"
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(320),unique=True,index=True)
    name: Mapped[str]=mapped_column(String(120))
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(10),default=Role.USER.value)

