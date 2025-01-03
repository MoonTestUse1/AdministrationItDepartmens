"""Requests CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict
from ..models.request import Request, RequestStatus
from ..schemas.request import RequestCreate

def create_request(db: Session, request: RequestCreate, employee_id: int) -> Request:
    """Create new request"""
    db_request = Request(
        department=request.department,
        request_type=request.request_type,
        description=request.description,
        priority=request.priority,
        status=RequestStatus.NEW,
        employee_id=employee_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_request(db: Session, request_id: int) -> Optional[Request]:
    """Get request by ID"""
    return db.query(Request).filter(Request.id == request_id).first()

def get_employee_requests(db: Session, employee_id: int) -> list[Request]:
    """Get employee's requests"""
    return db.query(Request).filter(Request.employee_id == employee_id).all()

def get_requests(db: Session, status: Optional[RequestStatus] = None, skip: int = 0, limit: int = 100) -> list[Request]:
    """Get all requests with optional status filter"""
    query = db.query(Request)
    if status:
        query = query.filter(Request.status == status)
    return query.offset(skip).limit(limit).all()

def update_request_status(db: Session, request_id: int, status: RequestStatus) -> Optional[Request]:
    """Update request status"""
    db_request = get_request(db, request_id)
    if db_request:
        db_request.status = status
        db.commit()
        db.refresh(db_request)
    return db_request

def get_statistics(db: Session) -> Dict:
    """Get request statistics"""
    total = db.query(func.count(Request.id)).scalar()
    
    # Получаем количество заявок по статусам
    status_counts = db.query(
        Request.status,
        func.count(Request.id)
    ).group_by(Request.status).all()
    
    # Инициализируем словарь всеми возможными статусами
    by_status = {
        RequestStatus.NEW: 0,
        RequestStatus.IN_PROGRESS: 0,
        RequestStatus.COMPLETED: 0,
        RequestStatus.REJECTED: 0
    }
    
    # Обновляем значения из базы
    for status, count in status_counts:
        by_status[status] = count
    
    return {
        "total": total or 0,
        "by_status": by_status
    }