from pydantic_settings import BaseSettings
class Settings(BaseSettings):database_url:str="postgresql+psycopg://payment:paymentpass@payment-db:5432/payments";jwt_secret:str="change-me"
settings=Settings()

