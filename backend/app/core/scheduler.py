from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.tasks.cleanup import cleanup_old_messages

scheduler = AsyncIOScheduler()

def setup_scheduler():
    """Настраивает планировщик задач"""
    
    # Запускаем очистку старых сообщений каждый день в полночь
    scheduler.add_job(
        cleanup_old_messages,
        trigger=CronTrigger(hour=0, minute=0),
        id='cleanup_old_messages',
        name='Cleanup old messages and files',
        replace_existing=True
    )

    scheduler.start() 