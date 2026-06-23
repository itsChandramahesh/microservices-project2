from fastapi import APIRouter,Depends
from .database import inventory
from .schemas import StockUpdate,Quantity,Stock
from .crud import get,reserve
from .auth import admin
router=APIRouter()
@router.get("/{product_id}",response_model=Stock)
async def stock(product_id:int):return await get(product_id)
@router.put("/{product_id}",response_model=Stock,dependencies=[Depends(admin)])
async def update(product_id:int,data:StockUpdate):
    await inventory.update_one({"product_id":product_id},{"$set":{"available_stock":data.available_stock},"$setOnInsert":{"reserved_stock":0}},upsert=True);return await get(product_id)
@router.post("/{product_id}/reserve",response_model=Stock)
async def reserve_(product_id:int,data:Quantity):return await reserve(product_id,data.quantity)
@router.post("/{product_id}/release",response_model=Stock)
async def release(product_id:int,data:Quantity):
    await inventory.update_one({"product_id":product_id,"reserved_stock":{"$gte":data.quantity}},{"$inc":{"available_stock":data.quantity,"reserved_stock":-data.quantity}});return await get(product_id)

