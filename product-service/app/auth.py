from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Header, HTTPException
from .config import settings
def token(subject: str, role: str="USER") -> str:
    return jwt.encode({"sub":subject,"role":role,"exp":datetime.now(timezone.utc)+timedelta(hours=8)},settings.jwt_secret,algorithm="HS256")
def claims(authorization: str=Header(...)) -> dict:
    try:
        scheme,value=authorization.split()
        if scheme.lower()!="bearer": raise ValueError
        return jwt.decode(value,settings.jwt_secret,algorithms=["HS256"])
    except Exception as exc: raise HTTPException(401,"Invalid token") from exc
def admin(data: dict=__import__("fastapi").Depends(claims)) -> dict:
    if data.get("role")!="ADMIN": raise HTTPException(403,"Admin role required")
    return data

