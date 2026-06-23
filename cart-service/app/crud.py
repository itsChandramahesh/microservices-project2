import json
from .database import redis
async def read(user_id:str):
    raw=await redis.get(f"cart:{user_id}");return json.loads(raw) if raw else []
async def write(user_id,items):await redis.set(f"cart:{user_id}",__import__("json").dumps(items))

