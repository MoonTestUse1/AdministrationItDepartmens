from aiogram import Bot, Dispatcher
from app.bot.config import settings

bot = Bot(token="7677506032:AAHB2QtrxKdgUXLWlE2xXaVxs9V7BPz1fhc")
dp = Dispatcher()
from .handlers import start, status


async def start_bot():
    """Start the bot"""
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
