from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:userpass@user-db:5432/users"
    jwt_secret: str = "change-me"
    service_name: str = "user-service"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()

