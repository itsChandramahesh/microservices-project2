from sqlalchemy.orm import Session
from .models import Category
def create(db:Session,data):
 obj=Category(**data.model_dump());db.add(obj);db.commit();db.refresh(obj);return obj

