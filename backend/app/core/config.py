"""Application configuration"""
import os
from typing import Any
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    # База данных
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "app"
    POSTGRES_TEST_DB: str = "test_app"

    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Режим тестирования
    TESTING: bool = bool(os.getenv("TESTING", ""))

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TEST_DB: int = 1

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "allow"
    }

    def get_database_url(self) -> str:
        """Get database URL"""
        # Получаем URL из переменной окружения, если она есть
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
            
        # Иначе формируем URL на основе настроек
        if self.TESTING:
            host = os.getenv("POSTGRES_HOST", "postgres")
            db = self.POSTGRES_TEST_DB
        else:
            host = self.POSTGRES_HOST
            db = self.POSTGRES_DB
            
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{host}:{self.POSTGRES_PORT}/{db}"

    def get_redis_url(self) -> str:
        """Get Redis URL"""
        db = self.REDIS_TEST_DB if self.TESTING else self.REDIS_DB
        host = "localhost" if self.TESTING else self.REDIS_HOST
        return f"redis://{host}:{self.REDIS_PORT}/{db}"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()

settings = get_settings() 