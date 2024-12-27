"""Bot initialization module"""
from aiogram import Bot, Dispatcher
from .config import settings
from .handlers import callbacks_router, start_router

# Initialize bot and dispatcher
bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# Include routers only once during initialization
dp.include_router(callbacks_router)
dp.include_router(start_router)

async def start_bot():
    """Start the bot"""
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"Error starting bot: {e}")