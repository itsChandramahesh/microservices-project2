from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    mongodb_url:str="mongodb://inventory-db:27017"; mongodb_db:str="inventory"; jwt_secret:str="change-me"
settings=Settings()

