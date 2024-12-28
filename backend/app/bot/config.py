"""Bot-specific configuration"""
from ..config import settings

BOT_TOKEN = settings.bot_token
CHAT_ID = settings.chat_id

# Request status constants
class RequestStatus:
    """Constants for request statuses"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"