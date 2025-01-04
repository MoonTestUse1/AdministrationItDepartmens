"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings"""
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "support"
    POSTGRES_HOST: str = "support-db"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: str = None  # Будет установлено в __init__

    # Redis settings
    REDIS_HOST: str = "support-redis"
    REDIS_PORT: int = 6379

    # JWT settings
    SECRET_KEY: str = "your-secret-key"  # В продакшене нужно заменить на безопасный ключ
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Telegram settings
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Формируем URL для подключения к базе данных
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = ConfigDict(
        env_file=".env",
        extra="allow",  # Разрешаем дополнительные поля
        case_sensitive=True  # Учитываем регистр
    )


settings = Settings()