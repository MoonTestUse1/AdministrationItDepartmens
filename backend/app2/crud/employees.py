from sqlalchemy.orm import Session
from ..models import employee as models
from ..schemas import tables
from ..utils.auth import get_password_hash


def get_employee(db: Session, employee_id: int):
    return db.query(tables.Employee).filter(tables.Employee.id == employee_id).first()


def get_employee_by_lastname(db: Session, last_name: str):
    return (
        db.query(tables.Employee).filter(tables.Employee.last_name == last_name).first()
    )


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tables.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: models.EmployeeCreate):
    hashed_password = get_password_hash(employee.password)
    db_employee = tables.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        department=employee.department,
        office=employee.office,
        password=hashed_password,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, data: dict):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        for key, value in data.items():
            if key == "password":
                value = get_password_hash(value)
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee
