from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AETHER FinOps Intelligence"
    ENVIRONMENT: str = "development"
    PORT: int = 8003
    DATABASE_URL: str = "sqlite:///./backend/data/aether.db"
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
