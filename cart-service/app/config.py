from pydantic_settings import BaseSettings
class Settings(BaseSettings): redis_url:str="redis://cart-db:6379/0";jwt_secret:str="change-me"
settings=Settings()

