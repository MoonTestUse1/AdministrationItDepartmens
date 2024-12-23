import asyncio
import uvicorn
from app.main import app
from app.bot import start_bot
from logging import getLogger

logger = getLogger(__name__)


async def run_bot():
    """Run Telegram bot"""
    try:
        await start_bot()
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)


async def run_api():
    """Run FastAPI application"""
    config = uvicorn.Config(app, host=["localhost", "185.139.70.62"], port=8080, reload=True)
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
