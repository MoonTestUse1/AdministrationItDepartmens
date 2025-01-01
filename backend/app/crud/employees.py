"""Employee CRUD operations"""
from sqlalchemy.orm import Session
from ..models.employee import Employee
from ..utils.loggers import auth_logger

def get_employee(db: Session, employee_id: int):
    """Get employee by ID"""
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_lastname(db: Session, last_name: str):
    """Get employee by last name"""
    return db.query(Employee).filter(Employee.last_name == last_name).first()

def create_employee(db: Session, employee_data: dict):
    """Create new employee"""
    try:
        db_employee = Employee(**employee_data)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        db.rollback()
        auth_logger.error(f"Error creating employee: {e}")
        raise