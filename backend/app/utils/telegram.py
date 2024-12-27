from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from datetime import datetime
from logging import getLogger
from .constants import (
    STATUS_LABELS, PRIORITY_LABELS, PRIORITY_EMOJI,
    DEPARTMENT_LABELS, REQUEST_TYPE_LABELS, REQUEST_TYPE_EMOJI
)

# Initialize logger
logger = getLogger(__name__)

# Initialize bot with token
bot = Bot(token="7677506032:AAHEqNUr1lIUfNVbLwaWIaPeKKShsCyz3eo")

# Chat ID for notifications 
CHAT_ID = "5057752127"

def create_status_keyboard(request_id: int, current_status: str) -> InlineKeyboardMarkup:
    """Create inline keyboard with status buttons"""
    status_transitions = {
        'new': ['in_progress'],
        'in_progress': ['resolved'],
        'resolved': ['closed'],
        'closed': []
    }

    buttons = []
    available_statuses = status_transitions.get(current_status, [])
    
    for status in available_statuses:
        callback_data = f"status_{request_id}_{status}"
        logger.debug(f"Creating button with callback_data: {callback_data}")
        buttons.append([
            InlineKeyboardButton(
                text=STATUS_LABELS[status],
                callback_data=callback_data
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    logger.debug(f"Created keyboard: {keyboard}")
    return keyboard

def format_request_message(request_data: dict) -> str:
    """Format request data into a message"""
    created_at = datetime.fromisoformat(request_data['created_at']).strftime('%d.%m.%Y %H:%M')
    
    # Get translated values
    department = DEPARTMENT_LABELS.get(request_data['department'], request_data['department'])
    request_type = REQUEST_TYPE_LABELS.get(request_data['request_type'], request_data['request_type'])
    priority = PRIORITY_LABELS.get(request_data['priority'], request_data['priority'])
    status = STATUS_LABELS.get(request_data.get('status', 'new'), 'Неизвестно')
    
    return (
        f"📋 <b>Заявка #{request_data['id']}</b>\n\n"
        f"👤 <b>Сотрудник:</b> {request_data['employee_last_name']} {request_data['employee_first_name']}\n"
        f"🏢 <b>Отдел:</b> {department}\n"
        f"🚪 <b>Кабинет:</b> {request_data['office']}\n"
        f"{REQUEST_TYPE_EMOJI.get(request_data['request_type'], '📝')} <b>Тип заявки:</b> {request_type}\n"
        f"{PRIORITY_EMOJI.get(request_data['priority'], '⚪')} <b>Приоритет:</b> {priority}\n\n"
        f"📝 <b>Описание:</b>\n{request_data['description']}\n\n"
        f"🕒 <b>Создана:</b> {created_at}\n"
        f"📊 <b>Статус:</b> {status}"
    )

async def send_request_notification(request_data: dict):
    """Send notification about request to Telegram"""
    try:
        message = format_request_message(request_data)
        keyboard = create_status_keyboard(request_data['id'], request_data.get('status', 'new'))
        
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}", exc_info=True)
        raise

def send_notification(request_data: dict):
    """Wrapper to run async notification in sync context"""
    try:
        asyncio.run(send_request_notification(request_data))
    except Exception as e:
        logger.error(f"Failed to send notification: {e}", exc_info=True)
        raise