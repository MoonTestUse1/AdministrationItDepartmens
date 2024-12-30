"""Bot-specific configuration"""
from ..config import settings
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = settings.bot_token
CHAT_ID = settings.chat_id

# Telegram API credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

# Request status constants
class RequestStatus:
    """Constants for request statuses"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"