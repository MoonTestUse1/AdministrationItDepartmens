from aiogram import types
from aiogram.filters import CommandStart
from ..bot import dp


@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Handle /start command"""
    await message.answer(
        "👋 Привет! Я бот технической поддержки.\n"
        "Я буду отправлять уведомления о новых заявках и позволю менять их статус."
    )
