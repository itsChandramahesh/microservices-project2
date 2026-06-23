from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .database import get_db
from . import crud,schemas
from .auth import claims,token,admin
from .models import User
from sqlalchemy import func,select
router=APIRouter()
@router.post("/register",response_model=schemas.UserOut,status_code=201)
def register(data:schemas.Register,db:Session=Depends(get_db)):
    if crud.by_email(db,data.email): raise HTTPException(409,"Email already registered")
    return crud.create(db,data)
@router.post("/login",response_model=schemas.Token)
def login(data:schemas.Login,db:Session=Depends(get_db)):
    user=crud.by_email(db,data.email)
    if not user or not crud.pwd.verify(data.password,user.password_hash): raise HTTPException(401,"Invalid credentials")
    return {"access_token":token(str(user.id),user.role)}
def current(data=Depends(claims),db:Session=Depends(get_db)):
    user=db.get(__import__("app.models",fromlist=["User"]).User,int(data["sub"]))
    if not user: raise HTTPException(404,"User not found")
    return user
@router.get("/me",response_model=schemas.UserOut)
def me(user=Depends(current)): return user
@router.put("/me",response_model=schemas.UserOut)
def edit(data:schemas.UpdateProfile,user=Depends(current),db:Session=Depends(get_db)): return crud.update(db,user,data)
@router.get("/admin/stats",dependencies=[Depends(admin)])
def stats(db:Session=Depends(get_db)):return {"total_users":db.scalar(select(func.count(User.id))) or 0}
