from fastapi import APIRouter, HTTPException

from .crud import read, write
from .schemas import CartItem

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/{user_id}")
async def view_cart(user_id: str):
    return {"user_id": user_id, "items": await read(user_id)}


@router.post("/{user_id}/items")
async def add_item(user_id: str, item: CartItem):
    items = await read(user_id)
    for existing in items:
        if existing["product_id"] == item.product_id:
            existing["quantity"] += item.quantity
            await write(user_id, items)
            return {"detail": "item added", "items": items}
    items.append(item.model_dump())
    await write(user_id, items)
    return {"detail": "item added", "items": items}


@router.put("/{user_id}/items/{product_id}")
async def update_item(user_id: str, product_id: int, item: CartItem):
    items = await read(user_id)
    for existing in items:
        if existing["product_id"] == product_id:
            existing["quantity"] = item.quantity
            await write(user_id, items)
            return {"detail": "item updated", "items": items}
    raise HTTPException(status_code=404, detail="item not found")


@router.delete("/{user_id}/items/{product_id}")
async def remove_item(user_id: str, product_id: int):
    items = await read(user_id)
    updated = [item for item in items if item["product_id"] != product_id]
    if len(updated) == len(items):
        raise HTTPException(status_code=404, detail="item not found")
    await write(user_id, updated)
    return {"detail": "item removed", "items": updated}


@router.delete("/{user_id}")
async def clear_cart(user_id: str):
    await write(user_id, [])
    return {"detail": "cart cleared"}
