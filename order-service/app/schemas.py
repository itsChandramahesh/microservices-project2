from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel,ConfigDict
class Item(BaseModel):product_id:int;quantity:int;unit_price:Decimal
class OrderOut(BaseModel):
 id:int;user_id:str;status:str;total:Decimal;created_at:datetime;items:list[Item]
 model_config=ConfigDict(from_attributes=True)
class Status(BaseModel):status:str

