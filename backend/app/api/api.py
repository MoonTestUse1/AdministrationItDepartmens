from fastapi import APIRouter
from app.api.endpoints import auth, admin, employees, requests, statistics, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(requests.router, prefix="/requests", tags=["requests"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"]) 