"""
Bot initialization module.
Creates bot and dispatcher instances.
"""
from aiogram import Bot, Dispatcher
from .config import BOT_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def start_bot():
    """
    Start the bot and include all routers.
    This function is called when the application starts.
    """
    from .handlers import router  # Import here to avoid circular imports
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)