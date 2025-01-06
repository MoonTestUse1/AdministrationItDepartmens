"""Employee CRUD operations"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
from ..utils.loggers import auth_logger

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    """Get all employees"""
    return db.query(Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Get employee by ID"""
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_credentials(db: Session, first_name: str, last_name: str) -> Optional[Employee]:
    """Get employee by first name and last name"""
    return db.query(Employee).filter(
        Employee.first_name == first_name,
        Employee.last_name == last_name
    ).first()

def create_employee(db: Session, employee: EmployeeCreate, hashed_password: str) -> Employee:
    """Create new employee"""
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        department=employee.department,
        office=employee.office,
        hashed_password=hashed_password,
        is_admin=employee.is_admin
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[Employee]:
    """Update employee data"""
    db_employee = get_employee(db, employee_id)
    if db_employee:
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Delete employee"""
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee