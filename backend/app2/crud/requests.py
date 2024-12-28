from sqlalchemy.orm import Session
from ..models import request as models
from ..schemas import tables
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..schemas import tables
from datetime import datetime


def create_request(db: Session, request: models.RequestCreate):
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
    return db_request


def get_requests(db: Session, skip: int = 0, limit: int = 100):
    requests = (
        db.query(
            tables.Request,
            tables.Employee.last_name.label("employee_last_name"),
            tables.Employee.first_name.label("employee_first_name"),
        )
        .join(tables.Employee)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": req[0].id,
            "employee_id": req[0].employee_id,
            "department": req[0].department,
            "request_type": req[0].request_type,
            "priority": req[0].priority,
            "status": req[0].status,
            "description": req[0].description,
            "created_at": req[0].created_at,
            "employee_last_name": req[1],
            "employee_first_name": req[2],
        }
        for req in requests
    ]


def get_requests_by_employee_lastname(db: Session, last_name: str):
    requests = (
        db.query(
            tables.Request,
            tables.Employee.last_name.label("employee_last_name"),
            tables.Employee.first_name.label("employee_first_name"),
        )
        .join(tables.Employee)
        .filter(tables.Employee.last_name.ilike(f"%{last_name}%"))
        .all()
    )

    return [
        {
            "id": req[0].id,
            "employee_id": req[0].employee_id,
            "department": req[0].department,
            "request_type": req[0].request_type,
            "priority": req[0].priority,
            "status": req[0].status,
            "description": req[0].description,
            "created_at": req[0].created_at,
            "employee_last_name": req[1],
            "employee_first_name": req[2],
        }
        for req in requests
    ]


def update_request_status(
    db: Session, request_id: int, new_status: models.RequestStatus
):
    try:
        db_request = (
            db.query(tables.Request).filter(tables.Request.id == request_id).first()
        )
        if not db_request:
            return None

        # Define valid status transitions
        valid_transitions = {
            models.RequestStatus.NEW: [models.RequestStatus.IN_PROGRESS],
            models.RequestStatus.IN_PROGRESS: [models.RequestStatus.RESOLVED],
            models.RequestStatus.RESOLVED: [models.RequestStatus.CLOSED],
            models.RequestStatus.CLOSED: [],
        }

        current_status = models.RequestStatus(db_request.status)
        if new_status not in valid_transitions[current_status]:
            raise ValueError(
                f"Invalid status transition from {current_status} to {new_status}"
            )

        db_request.status = new_status
        db.commit()
        db.refresh(db_request)
        return db_request

    except Exception as e:
        db.rollback()
        raise e


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
        "employee_last_name": request.employee.last_name,
        "employee_first_name": request.employee.first_name,
        "department": request.department,
        "office": request.employee.office,
        "request_type": request.request_type,
        "priority": request.priority,
        "description": request.description,
        "status": request.status,
        "created_at": request.created_at.isoformat(),
    }


from sqlalchemy.orm import Session
from ..schemas import tables
from datetime import datetime


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
        "employee_last_name": request.employee.last_name,
        "employee_first_name": request.employee.first_name,
        "department": request.department,
        "office": request.employee.office,
        "request_type": request.request_type,
        "priority": request.priority,
        "description": request.description,
        "status": request.status,
        "created_at": request.created_at.isoformat(),
    }


def update_request_status(db: Session, request_id: int, new_status: str):
    """Update request status with validation"""
    try:
        # Define valid status transitions
        valid_transitions = {
            "new": ["in_progress"],
            "in_progress": ["resolved"],
            "resolved": ["closed"],
            "closed": [],
        }

        db_request = (
            db.query(tables.Request).filter(tables.Request.id == request_id).first()
        )
        if not db_request:
            return None

        current_status = db_request.status
        if new_status not in valid_transitions.get(current_status, []):
            raise ValueError(
                f"Invalid status transition from {current_status} to {new_status}"
            )

        db_request.status = new_status
        db.commit()
        db.refresh(db_request)

        # Get full request details after update
        return get_request_details(db, request_id)

    except Exception as e:
        db.rollback()
        raise e
