"""
Configuration module for the Telegram bot.
Contains all necessary settings and constants.
"""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Bot configuration settings"""
    bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    chat_id: str = Field(..., alias="TELEGRAM_CHAT_ID")
    database_url: str = Field(..., alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in environment

# Create settings instance
settings = Settings()

# Request status constants
class RequestStatus:
    """Constants for request statuses"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"