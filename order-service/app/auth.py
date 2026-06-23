import jwt
from fastapi import Header,HTTPException
from .config import settings
def claims(authorization:str=Header(...)):
 try:
  return jwt.decode(authorization.split()[1],settings.jwt_secret,algorithms=["HS256"])
 except Exception as exc:raise HTTPException(401,"Invalid token") from exc
def admin(c=__import__("fastapi").Depends(claims)):
 if c.get("role")!="ADMIN":raise HTTPException(403,"Admin role required")
 return c

