from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict
class PaymentCreate(BaseModel):order_id:int;amount:Decimal=Field(gt=0);succeed:bool=True
class PaymentOut(BaseModel):
 id:int;order_id:int;user_id:str;amount:Decimal;status:str;created_at:datetime
 model_config=ConfigDict(from_attributes=True)

