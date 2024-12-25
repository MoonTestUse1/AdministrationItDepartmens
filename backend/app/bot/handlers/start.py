"""Handler for start command and other basic commands"""
from aiogram import Router, types
from aiogram.filters import Command
from ..config import settings

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    await message.answer("Бот для обработки заявок запущен!")