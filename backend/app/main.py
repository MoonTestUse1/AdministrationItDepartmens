"""Main FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.base import Base
from .database import engine
from .routers import auth, requests, employees
from .websockets.notifications import notification_manager

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support API",
    description="API для системы поддержки IT-отдела",
    version="1.0.0"
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])

# Добавляем WebSocket маршруты
app.websocket("/api/ws/admin")(notification_manager.admin_endpoint)
app.websocket("/api/ws/employee/{employee_id}")(notification_manager.employee_endpoint)

@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    logger.info("Starting up application...")
    # Здесь можно добавить дополнительную инициализацию

@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    logger.info("Shutting down application...")