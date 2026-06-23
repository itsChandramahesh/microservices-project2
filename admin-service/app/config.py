from pydantic_settings import BaseSettings
class Settings(BaseSettings):
 database_url:str="postgresql+psycopg://admin:adminpass@admin-db:5432/admin";jwt_secret:str="change-me";user_service_url:str="http://user-service:8000";product_service_url:str="http://product-service:8000";order_service_url:str="http://order-service:8000";payment_service_url:str="http://payment-service:8000"
settings=Settings()
