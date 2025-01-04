"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.core.scheduler import setup_scheduler
from app.websockets.chat import handle_chat_connection

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(api_router, prefix=settings.api_v1_str)

# WebSocket для чата
app.add_api_websocket_route("/ws/chat", handle_chat_connection)

@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    setup_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    from app.core.scheduler import scheduler
    scheduler.shutdown()