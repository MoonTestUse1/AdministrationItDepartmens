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
        f"📋 <b>Заявка #{request_data['id']}</b>\n\n"
        f"👤 <b>Сотрудник:</b> {request_data['employee_last_name']} {request_data['employee_first_name']}\n"
        f"🏢 <b>Отдел:</b> {department}\n"
        f"🚪 <b>Кабинет:</b> {request_data['office']}\n"
        f"{REQUEST_TYPE_EMOJI.get(request_data['request_type'], '📝')} <b>Тип заявки:</b> {request_type}\n"
        f"{PRIORITY_EMOJI.get(request_data['priority'], '⚪')} <b>Приоритет:</b> {priority}\n\n"
        f"📝 <b>Описание:</b>\n<blockquote>{request_data['description']}</blockquote>\n\n"
        f"🕒 <b>Создана:</b> {created_at}\n"
        f"📊 <b>Статус:</b> {status}"
    )
    
    try:
        await bot.send_message(
            chat_id=NOTIFICATION_CHAT_ID,
            text=message_text,
            reply_markup=get_updated_keyboard(request_data['id'], "new")
        )
    except Exception as e:
        print(f"Error sending notification: {e}")