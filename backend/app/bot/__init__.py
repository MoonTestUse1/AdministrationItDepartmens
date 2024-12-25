"""Bot initialization module"""
from aiogram import Bot, Dispatcher
from .config import settings

# Initialize bot and dispatcher
bot = Bot(token=settings.bot_token)
dp = Dispatcher()

async def start_bot():
    """Start the bot and include all routers"""
    from .handlers import callbacks_router, start_router
    
    # Include routers
    dp.include_router(callbacks_router)
    dp.include_router(start_router)
    
    # Start polling
    await dp.start_polling(bot, skip_updates=True)