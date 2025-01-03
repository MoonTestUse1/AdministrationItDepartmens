from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/support_db"
    REDIS_URL: str = "redis://redis:6379/0"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key"  # в продакшене использовать сложный ключ
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Telegram settings
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings() 