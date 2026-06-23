from pydantic import BaseModel, EmailStr, Field, ConfigDict
class Register(BaseModel):
    email: EmailStr
    name: str=Field(min_length=2,max_length=120)
    password: str=Field(min_length=8,max_length=128)
class Login(BaseModel): email: EmailStr; password: str
class UpdateProfile(BaseModel): name: str|None=Field(None,min_length=2,max_length=120); password: str|None=Field(None,min_length=8,max_length=128)
class UserOut(BaseModel):
    id:int; email:EmailStr; name:str; role:str
    model_config=ConfigDict(from_attributes=True)
class Token(BaseModel): access_token:str; token_type:str="bearer"

