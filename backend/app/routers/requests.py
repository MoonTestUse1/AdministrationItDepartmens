"""Request handling routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import requests as requests_crud
from ..models.request import RequestCreate
from ..bot.notifications import send_notification
from logging import getLogger

router = APIRouter()
logger = getLogger(__name__)

@router.post("/")
async def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    """Create new request"""
    try:
        db_request = requests_crud.create_request(db, request)
        # Send notification to Telegram
        await send_notification(requests_crud.get_request_details(db, db_request.id))
        return db_request
    except Exception as e:
        logger.error(f"Error creating request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при создании заявки")

@router.get("/")
async def get_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all requests"""
    try:
        return requests_crud.get_requests(db, skip, limit)
    except Exception as e:
        logger.error(f"Error fetching requests: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при получении заявок")

@router.get("/{request_id}")
async def get_request(request_id: int, db: Session = Depends(get_db)):
    """Get request by ID"""
    try:
        request = requests_crud.get_request_details(db, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Заявка не найдена")
        return request
    except Exception as e:
        logger.error(f"Error fetching request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при получении заявки")