"""Request CRUD operations"""
from sqlalchemy.orm import Session
from ..models.request import Request
from ..schemas.request import RequestCreate
from ..utils.loggers import request_logger

def create_request(db: Session, request: RequestCreate):
    """Create new request"""
    try:
        db_request = Request(
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
        "department": request.department,
        "office": request.employee.office,
        "request_type": request.request_type,
        "priority": request.priority,
        "description": request.description,
        "status": request.status,
        "created_at": request.created_at.isoformat()
    }