"""Settings configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "Support Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres123@db:5432/support_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "your-bot-token"
    TELEGRAM_CHAT_ID: str = "your-chat-id"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings() 