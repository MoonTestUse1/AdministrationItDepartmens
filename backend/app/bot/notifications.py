"""
Notifications module for the Telegram bot.
Handles sending notifications about new requests and status updates.
"""
from aiogram import types
from .config import settings  # Изменено с NOTIFICATION_CHAT_ID на settings
from . import bot
from .handlers import get_updated_keyboard

# Константы для эмодзи
REQUEST_TYPE_EMOJI = {
    "hardware": "🔧",
    "software": "💻",
    "network": "🌐",
    "other": "📝"
}

PRIORITY_EMOJI = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢"
}

async def send_notification(request_data: dict):
    """
    Send notification about new request to Telegram chat.
    
    Args:
        request_data (dict): Request data including id, description, etc.
    """
    message_text = (
        f"📋 <b>Заявка #{request_data['id']}</b>\n\n"
        f"👤 <b>Сотрудник:</b> {request_data['employee_last_name']} {request_data['employee_first_name']}\n"
        f"🏢 <b>Отдел:</b> {request_data['department']}\n"
        f"🚪 <b>Кабинет:</b> {request_data['office']}\n"
        f"{REQUEST_TYPE_EMOJI.get(request_data['request_type'], '📝')} <b>Тип заявки:</b> {request_data['request_type']}\n"
        f"{PRIORITY_EMOJI.get(request_data['priority'], '⚪')} <b>Приоритет:</b> {request_data['priority']}\n\n"
        f"📝 <b>Описание:</b>\n{request_data['description']}\n\n"
        f"🕒 <b>Создана:</b> {request_data['created_at']}"
    )
    
    try:
        await bot.send_message(
            chat_id=settings.chat_id,  # Используем settings.chat_id вместо NOTIFICATION_CHAT_ID
            text=message_text,
            parse_mode="HTML",
            reply_markup=get_updated_keyboard(request_data['id'], "new")
        )
    except Exception as e:
        print(f"Error sending notification: {e}")