from pydantic_settings import BaseSettings
class Settings(BaseSettings):
 user_service_url:str="http://user-service:8000";product_service_url:str="http://product-service:8000";cart_service_url:str="http://cart-service:8000";inventory_service_url:str="http://inventory-service:8000";order_service_url:str="http://order-service:8000";payment_service_url:str="http://payment-service:8000";admin_service_url:str="http://admin-service:8000"
settings=Settings()

