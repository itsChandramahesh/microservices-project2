from pydantic import BaseModel,ConfigDict,Field
class CategoryIn(BaseModel):name:str=Field(min_length=1,max_length=100);description:str=""
class CategoryOut(CategoryIn):
 id:int
 model_config=ConfigDict(from_attributes=True)

