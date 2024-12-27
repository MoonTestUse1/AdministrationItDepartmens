"""Notifications module for the Telegram bot"""
from .config import settings
from . import bot
from .handlers import get_updated_keyboard

async def send_notification(request_data: dict):
    """Send notification about new request to Telegram chat"""
    message_text = (
        f"Новая заявка №{request_data['id']}\n"
        f"Отдел: {request_data['department']}\n"
        f"Тип: {request_data['request_type']}\n"
        f"Приоритет: {request_data['priority']}\n"
        f"Описание: {request_data['description']}"
    )
    
    try:
        await bot.send_message(
            chat_id=settings.chat_id,
            text=message_text,
            reply_markup=get_updated_keyboard(request_data['id'], "new")
        )
    except Exception as e:
        print(f"Error sending notification: {e}")