"""Application configuration module"""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    database_url: str = Field(..., alias="DATABASE_URL")
    bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    chat_id: str = Field(..., alias="TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()