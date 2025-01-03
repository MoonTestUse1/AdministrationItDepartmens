"""Request CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from ..models.request import Request, RequestStatus
from ..schemas.request import RequestCreate, RequestUpdate
from ..utils.loggers import request_logger
from typing import List, Optional
from enum import Enum

def create_request(db: Session, request: RequestCreate, employee_id: int):
    """Create new request"""
    try:
        db_request = Request(
            title=request.title,
            description=request.description,
            priority=request.priority.value,
            status=request.status.value,
            employee_id=employee_id
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        
        request_logger.info(
            "Request created",
            extra={"request_id": db_request.id}
        )
        
        return db_request
        
    except Exception as e:
        db.rollback()
        request_logger.error(f"Error creating request: {e}", exc_info=True)
        raise

def get_request_details(db: Session, request_id: int):
    """Get detailed request information including employee details"""
    request = (
        db.query(Request)
        .join(Request.employee)
        .filter(Request.id == request_id)
        .first()
    )

    if not request:
        return None

    return {
        "id": request.id,
        "employee_id": request.employee_id,
        "employee_last_name": request.employee.last_name,
        "employee_first_name": request.employee.first_name,
        "title": request.title,
        "description": request.description,
        "priority": request.priority,
        "status": request.status,
        "created_at": request.created_at.isoformat()
    }

def get_requests(db: Session, skip: int = 0, limit: int = 100) -> List[Request]:
    """Get all requests with pagination"""
    return db.query(Request).offset(skip).limit(limit).all()

def get_request(db: Session, request_id: int) -> Optional[Request]:
    """Get request by ID"""
    return db.query(Request).filter(Request.id == request_id).first()

def get_employee_requests(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[Request]:
    """Get requests by employee ID"""
    return db.query(Request).filter(Request.employee_id == employee_id).offset(skip).limit(limit).all()

def update_request(db: Session, request_id: int, request: RequestUpdate):
    """Update request"""
    db_request = get_request(db, request_id)
    if not db_request:
        return None
        
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if isinstance(value, Enum):
            value = value.value
        setattr(db_request, field, value)
        
    db.commit()
    db.refresh(db_request)
    return db_request

def delete_request(db: Session, request_id: int):
    """Delete request"""
    db_request = get_request(db, request_id)
    if db_request:
        db.delete(db_request)
        db.commit()
    return db_request

def get_statistics(db: Session):
    """Get requests statistics"""
    # Прямой SQL запрос для проверки таблицы
    sql_check = db.execute(text("SELECT * FROM requests")).fetchall()
    request_logger.info(f"Direct SQL check - all requests: {sql_check}")
    
    # Проверяем структуру таблицы
    table_info = db.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'requests'
    """)).fetchall()
    request_logger.info(f"Table structure: {table_info}")
    
    # Проверяем все заявки через ORM
    all_requests = db.query(Request).all()
    request_logger.info(f"ORM check - Found {len(all_requests)} requests")
    
    for req in all_requests:
        request_logger.info(
            f"Request #{req.id}: "
            f"title='{req.title}', "
            f"status='{req.status}', "
            f"priority='{req.priority}', "
            f"employee_id={req.employee_id}"
        )
    
    # Подсчитываем статусы
    status_counts = {
        RequestStatus.NEW.value: 0,
        RequestStatus.IN_PROGRESS.value: 0,
        RequestStatus.COMPLETED.value: 0,
        RequestStatus.REJECTED.value: 0
    }
    
    # Прямой подсчет через SQL
    for status in RequestStatus:
        count = db.execute(
            text(f"SELECT COUNT(*) FROM requests WHERE status = :status"),
            {"status": status.value}
        ).scalar()
        status_counts[status.value] = count
        request_logger.info(f"SQL count for status {status.value}: {count}")
    
    result = {
        "total": len(all_requests),
        "new": status_counts[RequestStatus.NEW.value],
        "in_progress": status_counts[RequestStatus.IN_PROGRESS.value],
        "completed": status_counts[RequestStatus.COMPLETED.value],
        "rejected": status_counts[RequestStatus.REJECTED.value]
    }
    
    request_logger.info(f"Status counts: {status_counts}")
    request_logger.info(f"Final statistics: {result}")
    return result