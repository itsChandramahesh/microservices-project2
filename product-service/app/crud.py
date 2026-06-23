from sqlalchemy import select,or_
from sqlalchemy.orm import Session
from .models import Product
def create(db:Session,data):
    obj=Product(**data.model_dump());db.add(obj);db.commit();db.refresh(obj);return obj
def list_(db:Session,q=None,category=None,offset=0,limit=20):
    stmt=select(Product)
    if q: stmt=stmt.where(or_(Product.name.ilike(f"%{q}%"),Product.description.ilike(f"%{q}%")))
    if category:stmt=stmt.where(Product.category==category)
    return list(db.scalars(stmt.offset(offset).limit(limit)))
def update(db,obj,data):
    for k,v in data.model_dump(exclude_unset=True).items():setattr(obj,k,v)
    db.commit();db.refresh(obj);return obj

