"""Telegram bot utils"""
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from datetime import datetime
import os
from logging import getLogger
from ..models.request import RequestStatus, RequestPriority

# Initialize logger
logger = getLogger(__name__)

# Initialize bot with token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "5057752127")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def format_priority(priority: str) -> str:
    """Format priority with emoji"""
    priority_emoji = {
        RequestPriority.LOW: "🟢",
        RequestPriority.MEDIUM: "🟡",
        RequestPriority.HIGH: "🔴"
    }
    return f"{priority_emoji.get(priority, '⚪')} {priority.capitalize()}"

def format_status(status: str) -> str:
    """Format status with emoji"""
    status_emoji = {
        RequestStatus.NEW: "🆕",
        RequestStatus.IN_PROGRESS: "⏳",
        RequestStatus.COMPLETED: "✅",
        RequestStatus.REJECTED: "❌"
    }
    return f"{status_emoji.get(status, '⚪')} {status.capitalize()}"

async def send_request_notification(request_data: dict):
    """Send notification about new request to Telegram"""
    try:
        message = (
            f"📋 <b>Новая заявка #{request_data['id']}</b>\n\n"
            f"📝 <b>Заголовок:</b> {request_data['title']}\n"
            f"👤 <b>Сотрудник:</b> {request_data.get('employee_name', 'Не указан')}\n"
            f"❗ <b>Приоритет:</b> {format_priority(request_data['priority'])}\n"
            f"📊 <b>Статус:</b> {format_status(request_data['status'])}\n\n"
            f"📄 <b>Описание:</b>\n{request_data['description']}\n\n"
            f"🕒 <b>Создана:</b> {request_data['created_at'].strftime('%d.%m.%Y %H:%M') if request_data['created_at'] else 'Не указано'}"
        )
        
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}", exc_info=True)

def notify_new_request(request_data: dict):
    """Wrapper to run async notification in sync context"""
    try:
        asyncio.run(send_request_notification(request_data))
    except Exception as e:
        logger.error(f"Failed to send notification: {e}", exc_info=True)

async def send_status_notification(request_id: int, new_status: str, employee_telegram_id: str):
    """Send notification about status change"""
    try:
        message = (
            f"🔄 <b>Обновление статуса заявки #{request_id}</b>\n\n"
            f"📊 <b>Новый статус:</b> {format_status(new_status)}"
        )
        
        await bot.send_message(
            chat_id=employee_telegram_id,
            text=message,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error sending status notification: {e}", exc_info=True)

def notify_status_change(request_id: int, new_status: str, employee_telegram_id: str):
    """Wrapper to run async status notification in sync context"""
    try:
        asyncio.run(send_status_notification(request_id, new_status, employee_telegram_id))
    except Exception as e:
        logger.error(f"Failed to send status notification: {e}", exc_info=True)