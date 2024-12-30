"""Notifications module for the Telegram bot"""
from .config import settings
from . import bot
from .handlers import get_updated_keyboard
from .messages import format_request_message



async def send_notification(request_data: dict):
    """Send notification about new request to Telegram chat"""
    try:
        message_text = format_request_message(request_data)
        await bot.send_message(
            chat_id=settings.chat_id,
            text=message_text,
            parse_mode="HTML",
            reply_markup=get_updated_keyboard(request_data['id'], "new")
        )
    except Exception as e:
        print(f"Error sending notification: {e}")
