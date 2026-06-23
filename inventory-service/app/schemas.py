from pydantic import BaseModel,Field
class StockUpdate(BaseModel): available_stock:int=Field(ge=0)
class Quantity(BaseModel): quantity:int=Field(gt=0)
class Stock(BaseModel): product_id:int;available_stock:int;reserved_stock:int

