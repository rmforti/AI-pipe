from pydantic_settings import BaseSettings

import os

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "AI Assistant"
    environment: str = "development"

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small",
)

MAX_UPLOAD_FILE_SIZE_BYTES = int(
    os.getenv("MAX_UPLOAD_FILE_SIZE_BYTES", "1000000")
)

SUPPORTED_UPLOAD_EXTENSIONS = (
    ".txt",
    ".md",
    ".pdf",
)


print("OPENAI_MODEL:", OPENAI_MODEL)
print("EMBEDDING_MODEL:", OPENAI_EMBEDDING_MODEL)
print("API KEY FOUND:", OPENAI_API_KEY is not None)

settings = Settings()