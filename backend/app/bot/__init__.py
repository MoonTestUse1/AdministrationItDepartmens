from aiogram import Bot, Dispatcher
from .config import BOT_TOKEN

bot = Bot(token="7677506032:AAHduD5EePz3bE23DKlo35KoOp2_9lZuS34")
dp = Dispatcher()

async def start_bot():
    # Импортируем здесь, чтобы избежать циклических импортов
    from .bot import router
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)