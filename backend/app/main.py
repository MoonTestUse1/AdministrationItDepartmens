"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import auth, employees, requests, admin
from .db.base import Base
from .database import engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Подключаем роутеры
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(employees.router, prefix=settings.API_V1_STR, tags=["employees"])
app.include_router(requests.router, prefix=settings.API_V1_STR, tags=["requests"])
app.include_router(admin.router, prefix=settings.API_V1_STR, tags=["admin"])