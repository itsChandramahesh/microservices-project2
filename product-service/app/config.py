from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://product:productpass@product-db:3306/products"
    jwt_secret: str = "change-me"
    service_name: str = "product-service"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()

