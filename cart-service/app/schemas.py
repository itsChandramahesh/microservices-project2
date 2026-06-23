from pydantic import BaseModel,Field
class CartItem(BaseModel):product_id:int;quantity:int=Field(gt=0)
class Cart(BaseModel):user_id:str;items:list[CartItem]

