"""Request management database operations"""
from sqlalchemy.orm import Session
from ..models import request as models
from ..schemas import tables
from ..utils.loggers import request_logger

def create_request(db: Session, request: models.RequestCreate):
    """Create new request"""
    try:
        db_request = tables.Request(
            employee_id=request.employee_id,
            department=request.department,
            request_type=request.request_type,
            priority=request.priority,
            description=request.description,
            status="new",
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
        db.query(tables.Request)
        .join(tables.Employee)
        .filter(tables.Request.id == request_id)
        .first()
    )

    if not request:
        return None

    return {
        "id": request.id,
        "employee_id": request.employee_id,
        "employee_last_name": request.employee.last_name,
        "employee_first_name": request.employee.first_name,
        "department": request.department,
        "office": request.employee.office,
        "request_type": request.request_type,
        "priority": request.priority,
        "description": request.description,
        "status": request.status,
        "created_at": request.created_at.isoformat()
    }