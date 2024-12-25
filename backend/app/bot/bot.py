from aiogram import Bot, Dispatcher
from app.bot.config import settings

bot = Bot(token="7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34")
dp = Dispatcher()
from .handlers import start, status


async def start_bot():
    """Start the bot"""
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
