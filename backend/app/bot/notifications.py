import asyncio
from logging import getLogger
from aiogram.client.session.aiohttp import AiohttpSession
from .bot import bot
from .keyboards import create_status_keyboard
from .messages import format_request_message
from .config import settings

logger = getLogger(__name__)


async def send_request_notification(request_data: dict):
    try:
        message = format_request_message(request_data)
        keyboard = create_status_keyboard(
            request_data["id"], request_data.get("status", "new")
        )

        async with AiohttpSession() as session:
            bot.session = session
            await bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}", exc_info=True)
        raise


def send_notification(request_data: dict):
    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_request_notification(request_data))
        loop.close()
    except Exception as e:
        logger.error(f"Failed to send notification: {e}", exc_info=True)
        raise
