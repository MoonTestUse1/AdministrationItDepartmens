"""Admin routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import crud, schemas
from ..utils.auth import get_current_admin

router = APIRouter()

@router.get("/statistics")
async def get_statistics(period: str = "week", db: Session = Depends(get_db)):
    """Get request statistics"""
    try:
        return statistics.get_statistics(db, period)
    except Exception as e:
        request_logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении статистики")

@router.get("/requests", response_model=List[schemas.Request])
async def get_all_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получить список всех заявок (только для админа)
    """
    try:
        requests = crud.requests.get_requests(db, skip=skip, limit=limit)
        return requests
    except Exception as e:
        print(f"Error getting requests: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/requests/{request_id}", response_model=schemas.Request)
async def get_request_by_id(
    request_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получить заявку по ID (только для админа)
    """
    request = crud.requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request