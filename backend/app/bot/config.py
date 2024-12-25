"""
Configuration module for the Telegram bot.
Contains all necessary settings and constants.
"""

# Bot token from environment variables
BOT_TOKEN = "7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34"

# Chat ID for notifications
NOTIFICATION_CHAT_ID = "-1002037023574"

# Request status constants
class RequestStatus:
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"