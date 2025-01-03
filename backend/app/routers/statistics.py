"""Statistics router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.request import Request, RequestStatus
from ..utils.loggers import request_logger

router = APIRouter()

@router.get("/")
def get_statistics(db: Session = Depends(get_db)):
    """Get request statistics"""
    # Получаем общее количество заявок
    total = db.query(Request).count()
    request_logger.info(f"Total requests: {total}")
    
    # Получаем количество заявок по статусам
    new_requests = db.query(Request).filter(Request.status == RequestStatus.NEW.value).count()
    in_progress = db.query(Request).filter(Request.status == RequestStatus.IN_PROGRESS.value).count()
    completed = db.query(Request).filter(Request.status == RequestStatus.COMPLETED.value).count()
    rejected = db.query(Request).filter(Request.status == RequestStatus.REJECTED.value).count()
    
    request_logger.info(f"Status counts - new: {new_requests}, in_progress: {in_progress}, completed: {completed}, rejected: {rejected}")
    
    result = {
        "total_requests": total,
        "by_status": {
            "new": new_requests,
            "in_progress": in_progress,
            "completed": completed,
            "rejected": rejected
        }
    }
    
    request_logger.info(f"Returning statistics: {result}")
    return result 