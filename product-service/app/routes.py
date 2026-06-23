from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import func,select
from .database import get_db
from .models import Product
from . import schemas,crud
from .auth import admin
router=APIRouter()
@router.get("/",response_model=list[schemas.ProductOut])
def products(q:str|None=None,category:str|None=None,page:int=Query(1,ge=1),size:int=Query(20,ge=1,le=100),db:Session=Depends(get_db)): return crud.list_(db,q,category,(page-1)*size,size)
@router.get("/admin/stats",dependencies=[Depends(admin)])
def stats(db:Session=Depends(get_db)):
 return {"total_products":db.scalar(select(func.count(Product.id))) or 0,"low_stock_products":[schemas.ProductOut.model_validate(x) for x in db.scalars(select(Product).where(Product.stock<10).limit(20))]}
@router.get("/{product_id}",response_model=schemas.ProductOut)
def product(product_id:int,db:Session=Depends(get_db)):
    if not (obj:=db.get(Product,product_id)):raise HTTPException(404,"Product not found")
    return obj
@router.post("/",response_model=schemas.ProductOut,status_code=201,dependencies=[Depends(admin)])
def create(data:schemas.ProductCreate,db:Session=Depends(get_db)):return crud.create(db,data)
@router.put("/{product_id}",response_model=schemas.ProductOut,dependencies=[Depends(admin)])
def update(product_id:int,data:schemas.ProductUpdate,db:Session=Depends(get_db)):
    if not (obj:=db.get(Product,product_id)):raise HTTPException(404,"Product not found")
    return crud.update(db,obj,data)
@router.delete("/{product_id}",status_code=204,dependencies=[Depends(admin)])
def delete(product_id:int,db:Session=Depends(get_db)):
    if not (obj:=db.get(Product,product_id)):raise HTTPException(404,"Product not found")
    db.delete(obj);db.commit()
@router.post("/bulk",response_model=list[schemas.ProductOut],dependencies=[Depends(admin)])
def bulk(items:list[schemas.ProductCreate],db:Session=Depends(get_db)):return [crud.create(db,x) for x in items]
