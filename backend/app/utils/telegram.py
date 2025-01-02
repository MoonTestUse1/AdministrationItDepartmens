"""Telegram bot utils"""
import os
from fastapi import APIRouter, Request
from telebot import TeleBot
from telebot.types import Update
from ..models.request import RequestStatus
from ..database import SessionLocal
from ..models.request import Request as DBRequest

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://itformhelp.ru/telegram/webhook/"
WEBHOOK_PATH = "/telegram/webhook/"

bot = TeleBot(TELEGRAM_BOT_TOKEN)
router = APIRouter()

@router.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    """Handle webhook from Telegram"""
    json_string = await request.json()
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return {"ok": True}

def setup_webhook():
    """Setup webhook"""
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

@bot.message_handler(commands=['start'])
def start(message):
    """Handle /start command"""
    bot.reply_to(message, "Привет! Я бот технической поддержки. Я буду уведомлять вас о статусе ваших заявок.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all messages"""
    bot.reply_to(message, "Я получил ваше сообщение и обязательно обработаю его!")

def notify_status_change(request_id: int, new_status: RequestStatus):
    """Notify user about request status change"""
    try:
        db = SessionLocal()
        request = db.query(DBRequest).filter(DBRequest.id == request_id).first()
        if request and request.employee and request.employee.telegram_id:
            status_messages = {
                RequestStatus.NEW: "создана",
                RequestStatus.IN_PROGRESS: "взята в работу",
                RequestStatus.COMPLETED: "выполнена",
                RequestStatus.REJECTED: "отклонена"
            }
            message = f"Статус вашей заявки №{request.id} изменен на: {status_messages.get(new_status, new_status)}"
            bot.send_message(request.employee.telegram_id, message)
    except Exception as e:
        print(f"Error sending telegram notification: {e}")
    finally:
        db.close()

# Инициализация вебхука при запуске
setup_webhook()