import asyncio
import uvicorn
from app.main import app
from app.bot import start_bot
from logging import getLogger

logger = getLogger(__name__)


async def run_bot():
    """Run Telegram bot"""
    print("Bot started")
    # try:
    #     await start_bot()
    # except Exception as e:
    #     logger.error(f"Bot crashed: {e}", exc_info=True)


async def run_api():
    """Run FastAPI application"""
    config = uvicorn.Config(app, host=["0.0.0.0"], port=8000, reload=True)
    server = uvicorn.Server(config)
    try:
        await server.serve()
    except Exception as e:
        logger.error(f"API crashed: {e}", exc_info=True)


async def run_all():
    """Run both bot and API"""
    await asyncio.gather(run_bot(), run_api())


if __name__ == "__main__":
    asyncio.run(run_all())
