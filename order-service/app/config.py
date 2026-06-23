from pydantic_settings import BaseSettings
class Settings(BaseSettings):
 database_url:str="postgresql+psycopg://order:orderpass@order-db:5432/orders";jwt_secret:str="change-me";cart_url:str="http://cart-service:8000";inventory_url:str="http://inventory-service:8000";product_url:str="http://product-service:8000"
settings=Settings()

