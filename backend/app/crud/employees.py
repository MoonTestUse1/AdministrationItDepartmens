"""Employee CRUD operations"""
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
from ..utils.loggers import auth_logger

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    """Get all employees"""
    return db.query(Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Get employee by ID"""
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_last_name(db: Session, last_name: str) -> Optional[Employee]:
    """Get employee by last name"""
    return db.query(Employee).filter(Employee.last_name == last_name).first()

def create_employee(db: Session, employee: EmployeeCreate, hashed_password: str) -> Employee:
    """Create new employee"""
    try:
        db_employee = Employee(
            first_name=employee.first_name,
            last_name=employee.last_name,
            department=employee.department,
            office=employee.office,
            hashed_password=hashed_password
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        auth_logger.error(f"Error creating employee: {e}")
        db.rollback()
        raise

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[Employee]:
    """Update employee"""
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
        
    for field, value in employee.model_dump(exclude_unset=True).items():
        setattr(db_employee, field, value)
        
    try:
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        auth_logger.error(f"Error updating employee: {e}")
        db.rollback()
        raise

def delete_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Delete employee"""
    db_employee = get_employee(db, employee_id)
    if db_employee:
        try:
            db.delete(db_employee)
            db.commit()
            return db_employee
        except Exception as e:
            auth_logger.error(f"Error deleting employee: {e}")
            db.rollback()
            raise
    return None