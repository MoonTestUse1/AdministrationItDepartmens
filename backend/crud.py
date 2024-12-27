from sqlalchemy.orm import Session
from models import request as models
from schemas import tables
from typing import List


def create_request(db: Session, request_data: dict):
    db_request = tables.Request(
        employee_id=request_data["employee_id"],
        department=request_data["department"],
        request_type=request_data["request_type"],
        priority=request_data["priority"],
        description=request_data["description"],
        status="new",
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_requests(db: Session, skip: int = 0, limit: int = 100) -> List[tables.Request]:
    return (
        db.query(tables.Request)
        .join(tables.Employee)
        .add_columns(
            tables.Employee.last_name.label("employee_last_name"),
            tables.Employee.first_name.label("employee_first_name"),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_requests_by_employee_lastname(
    db: Session, last_name: str
) -> List[tables.Request]:
    return (
        db.query(tables.Request)
        .join(tables.Employee)
        .filter(tables.Employee.last_name.ilike(f"%{last_name}%"))
        .all()
    )


def update_request_status(db: Session, request_id: int, new_status: str):
    db_request = (
        db.query(tables.Request).filter(tables.Request.id == request_id).first()
    )
    if db_request:
        db_request.status = new_status
        db.commit()
        db.refresh(db_request)
    return db_request
