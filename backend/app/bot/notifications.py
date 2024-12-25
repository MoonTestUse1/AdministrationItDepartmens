"""
Notifications module for the Telegram bot.
Handles sending notifications about new requests and status updates.
"""
from aiogram import types
from .config import NOTIFICATION_CHAT_ID
from . import bot
from .handlers import get_updated_keyboard

async def send_notification(request_data: dict):
    """
    Send notification about new request to Telegram chat.
    
    Args:
        request_data (dict): Request data including id, description, etc.
    """
    message_text = (
        f"Новая заявка №{request_data['id']}\n"
        f"Отдел: {request_data['department']}\n"
        f"Тип: {request_data['request_type']}\n"
        f"Приоритет: {request_data['priority']}\n"
        f"Описание: {request_data['description']}"
    )
    
    try:
        await bot.send_message(
            chat_id=NOTIFICATION_CHAT_ID,
            text=message_text,
            reply_markup=get_updated_keyboard(request_data['id'], "new")
        )
    except Exception as e:
        print(f"Error sending notification: {e}")