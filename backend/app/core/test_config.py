"""Test settings configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class TestSettings(BaseSettings):
    """Test application settings"""
    PROJECT_NAME: str = "Support Service Test"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///:memory:"
    
    # JWT
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "test-bot-token"
    TELEGRAM_CHAT_ID: str = "test-chat-id"

    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

test_settings = TestSettings() 