from fastapi import HTTPException
from .database import inventory
async def get(product_id:int):
    doc=await inventory.find_one({"product_id":product_id},{"_id":0})
    if not doc: raise HTTPException(404,"Inventory not found")
    return doc
async def reserve(product_id:int,quantity:int):
    result=await inventory.find_one_and_update({"product_id":product_id,"available_stock":{"$gte":quantity}},{"$inc":{"available_stock":-quantity,"reserved_stock":quantity}},return_document=True,projection={"_id":0})
    if not result:raise HTTPException(409,"Insufficient stock")
    return result

