import os
from pydantic_settings import BaseSettings
from typing import Optional
from typing import List


class Settings(BaseSettings):
    #Application configuration settings.

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "User Management API"

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./user_management.db")
    DB_ECHO_LOG: bool = os.getenv("DB_ECHO_LOG", "False").lower() == "true"

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://localhost:3000",  # Frontend
        "https://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
