from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict
class ProductBase(BaseModel):
    name:str=Field(min_length=1,max_length=200); description:str=""; price:Decimal=Field(gt=0); stock:int=Field(ge=0); category:str=Field(min_length=1,max_length=100); image_url:str|None=None
class ProductCreate(ProductBase): pass
class ProductUpdate(BaseModel):
    name:str|None=None;description:str|None=None;price:Decimal|None=Field(None,gt=0);stock:int|None=Field(None,ge=0);category:str|None=None;image_url:str|None=None
class ProductOut(ProductBase):
    id:int
    model_config=ConfigDict(from_attributes=True)

