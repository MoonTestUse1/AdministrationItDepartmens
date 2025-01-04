"""Main FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.base import Base
from .database import engine
from .routers import auth, requests, employees, admin, statistics
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
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])

# Добавляем WebSocket маршруты
@app.websocket("/api/ws/admin")
async def admin_websocket(websocket):
    await notification_manager.admin_endpoint(websocket)

@app.websocket("/api/ws/employee/{employee_id}")
async def employee_websocket(websocket, employee_id: int):
    await notification_manager.employee_endpoint(websocket, employee_id)

@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    logger.info("Starting up application...")
    # Здесь можно добавить дополнительную инициализацию

@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    logger.info("Shutting down application...")