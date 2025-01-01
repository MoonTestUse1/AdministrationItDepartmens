"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.request import Request, RequestStatus, RequestPriority
from ..schemas.request import RequestCreate, RequestResponse, RequestUpdate, RequestStatistics
from ..utils.auth import get_current_admin, get_current_employee
from sqlalchemy import func

router = APIRouter()

def request_to_dict(request: Request) -> dict:
    """Convert Request model to dictionary"""
    return {
        "id": request.id,
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "status": request.status,
        "employee_id": request.employee_id,
        "created_at": request.created_at,
        "updated_at": request.updated_at
    }

@router.get("/", response_model=List[RequestResponse])
def get_requests(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all requests"""
    try:
        requests = db.query(Request).all()
        return [request_to_dict(request) for request in requests]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=RequestResponse)
def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Create new request"""
    try:
        db_request = Request(
            title=request.title,
            description=request.description,
            priority=request.priority,
            status=RequestStatus.NEW.value,
            employee_id=current_employee["id"]
        )
        
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        return request_to_dict(db_request)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my", response_model=List[RequestResponse])
def get_employee_requests(
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Get employee's requests"""
    try:
        requests = db.query(Request).filter(
            Request.employee_id == current_employee["id"]
        ).all()
        
        # Преобразуем объекты в словари до закрытия сессии
        return [request_to_dict(request) for request in requests]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{request_id}/status", response_model=RequestResponse)
def update_request_status(
    request_id: int,
    status_update: RequestUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update request status"""
    try:
        db_request = db.query(Request).filter(Request.id == request_id).first()
        if not db_request:
            raise HTTPException(status_code=404, detail="Заявка не найдена")
        
        db_request.status = status_update.status
        db.commit()
        db.refresh(db_request)
        
        return request_to_dict(db_request)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin", response_model=List[RequestResponse])
def get_all_requests(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all requests with optional status filter"""
    try:
        query = db.query(Request)
        if status:
            query = query.filter(Request.status == status)
        requests = query.all()
        
        # Преобразуем объекты в словари до закрытия сессии
        return [request_to_dict(request) for request in requests]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
def get_request_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get request statistics"""
    try:
        total_requests = db.query(Request).count()
        
        # Статистика по статусам
        status_stats = db.query(
            Request.status,
            func.count(Request.id)
        ).group_by(Request.status).all()
        
        # Статистика по приоритетам
        priority_stats = db.query(
            Request.priority,
            func.count(Request.id)
        ).group_by(Request.priority).all()
        
        return {
            "total_requests": total_requests,
            "by_status": {
                status: count for status, count in status_stats
            },
            "by_priority": {
                priority: count for priority, count in priority_stats
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))