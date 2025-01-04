"""
Main application entry point.
Runs both the FastAPI application and Telegram bot.
"""
import asyncio
import uvicorn
from app.main import app
from app.bot import start_bot
from logging import getLogger

logger = getLogger(__name__)

async def run_api():
    """Run FastAPI application"""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Run both bot and API in the main thread"""
    try:
        # Создаем задачи для бота и API
        bot_task = asyncio.create_task(start_bot())
        api_task = asyncio.create_task(run_api())
        
        # Запускаем обе задачи
        await asyncio.gather(bot_task, api_task)
    except Exception as e:
        logger.error(f"Application crashed: {e}", exc_info=True)

if __name__ == "__main__":
    # Запускаем в основном потоыы
    asyncio.run(main())