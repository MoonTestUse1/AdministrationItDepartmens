"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import admin, employees, requests, auth, statistics

app = FastAPI(
    # Включаем автоматическое перенаправление со слэшем
    redirect_slashes=True,
    # Добавляем описание API
    title="Support System API",
    description="API для системы поддержки",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    "http://185.139.70.62",  # Добавляем ваш production домен
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])