"""
Configuration module for the Telegram bot.
Contains all necessary settings and constants.
"""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Bot configuration settings"""
    bot_token: str = Field("7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34", env="TELEGRAM_BOT_TOKEN")
    chat_id: str = Field("-1002037023574", env="TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

# Request status constants
class RequestStatus:
    """Constants for request statuses"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"