"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routers import auth, employees, requests, admin
from .database import engine, Base
from .db.init_db import init_db
from .database import get_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Создаем приложение
app = FastAPI(title="Employee Request System API")

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
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Инициализируем базу данных
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db = next(get_db())
    try:
        init_db(db)
    finally:
        db.close()