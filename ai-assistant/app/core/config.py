from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Assistant"
    environment: str = "development"

import os

import os

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small",
)

settings = Settings()