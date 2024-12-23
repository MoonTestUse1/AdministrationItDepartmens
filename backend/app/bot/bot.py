from aiogram import Bot, Dispatcher
from app.bot.config import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
from .handlers import start, status


async def start_bot():
    """Start the bot"""
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
