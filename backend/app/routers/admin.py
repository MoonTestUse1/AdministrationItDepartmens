"""Admin routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import statistics, requests
from ..utils.loggers import request_logger

router = APIRouter()

@router.get("/statistics")
async def get_statistics(period: str = "week", db: Session = Depends(get_db)):
    """Get request statistics"""
    try:
        return statistics.get_statistics(db, period)
    except Exception as e:
        request_logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении статистики")

@router.get("/requests")
async def get_all_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all requests with employee details"""
    try:
        return requests.get_requests(db, skip=skip, limit=limit)
    except Exception as e:
        request_logger.error(f"Error getting requests: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении заявок")