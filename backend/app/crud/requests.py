"""Requests CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict
from ..models.request import Request, RequestStatus
from ..schemas.request import RequestCreate
from . import employees

def create_request(db: Session, request: RequestCreate, employee_id: int) -> Request:
    """Create new request"""
    # Получаем данные сотрудника
    employee = employees.get_employee(db, employee_id)
    if not employee:
        raise ValueError("Employee not found")

    db_request = Request(
        department=employee.department,  # Берем отдел из данных сотрудника
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

def get_request_details(db: Session, request_id: int) -> Optional[Dict]:
    """Get detailed request information including employee data"""
    request = get_request(db, request_id)
    if not request:
        return None
    
    employee = employees.get_employee(db, request.employee_id)
    if not employee:
        return None
    
    return {
        "id": request.id,
        "request_type": request.request_type,
        "description": request.description,
        "priority": request.priority,
        "status": request.status,
        "department": request.department,
        "created_at": request.created_at.isoformat(),
        "employee_first_name": employee.first_name,
        "employee_last_name": employee.last_name
    }

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
    by_status = dict(
        db.query(
            Request.status,
            func.count(Request.id)
        ).group_by(Request.status).all()
    )
    return {
        "total": total,
        "by_status": by_status
    }