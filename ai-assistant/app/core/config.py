from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Assistant"
    environment: str = "development"


settings = Settings()