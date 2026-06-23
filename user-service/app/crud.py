from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User
from .schemas import Register,UpdateProfile
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def by_email(db:Session,email:str): return db.scalar(select(User).where(User.email==email))
def create(db:Session,data:Register,role:str="USER"):
    user=User(email=data.email.lower(),name=data.name,password_hash=pwd.hash(data.password),role=role); db.add(user); db.commit(); db.refresh(user); return user
def update(db:Session,user:User,data:UpdateProfile):
    if data.name is not None:user.name=data.name
    if data.password is not None:user.password_hash=pwd.hash(data.password)
    db.commit();db.refresh(user);return user

