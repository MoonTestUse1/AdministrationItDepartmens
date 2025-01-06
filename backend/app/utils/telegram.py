"""Telegram bot utils"""
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from datetime import datetime
from logging import getLogger
from ..models.request import RequestStatus, RequestPriority
from ..crud import requests
from ..database import get_db
from ..core.config import settings

# Initialize logger
logger = getLogger(__name__)

# Initialize bot with token from settings
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

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

async def send_request_notification(request_id: int):
    """Send notification about new request to Telegram"""
    try:
        # Получаем данные заявки
        db = next(get_db())
        request_data = requests.get_request_details(db, request_id)
        if not request_data:
            logger.error(f"Request {request_id} not found")
            return

        message = (
            f"📋 <b>Новая заявка #{request_data['id']}</b>\n\n"
            f"👤 <b>Сотрудник:</b> {request_data['employee_first_name']} {request_data['employee_last_name']}\n"
            f"🏢 <b>Отдел:</b> {request_data['department']}\n"
            f"📝 <b>Тип заявки:</b> {request_data['request_type']}\n"
            f"❗ <b>Приоритет:</b> {format_priority(request_data['priority'])}\n"
            f"📊 <b>Статус:</b> {format_status(request_data['status'])}\n\n"
            f"📄 <b>Описание:</b>\n{request_data['description']}\n\n"
            f"🕒 <b>Создана:</b> {datetime.fromisoformat(request_data['created_at']).strftime('%d.%m.%Y %H:%M')}"
        )
        
        await bot.send_message(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}", exc_info=True)

async def notify_new_request(request_id: int):
    """Async wrapper for send_request_notification"""
    await send_request_notification(request_id)

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

async def notify_status_change(request_id: int, new_status: str, employee_telegram_id: str):
    """Async wrapper for send_status_notification"""
    await send_status_notification(request_id, new_status, employee_telegram_id)