"""Statistics router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.request import Request, RequestStatus

router = APIRouter()

@router.get("/")
def get_statistics(db: Session = Depends(get_db)):
    """Get request statistics"""
    # Получаем количество заявок по статусам
    new_requests = db.query(Request).filter(Request.status == RequestStatus.NEW).count()
    in_progress = db.query(Request).filter(Request.status == RequestStatus.IN_PROGRESS).count()
    resolved = db.query(Request).filter(Request.status == RequestStatus.RESOLVED).count()
    
    return {
        "new": new_requests,
        "inProgress": in_progress,
        "resolved": resolved
    } 