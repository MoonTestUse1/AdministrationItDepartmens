"""Employee management database operations"""
from sqlalchemy.orm import Session
from ..models import employee as models
from ..schemas import tables
from ..utils.auth import get_password_hash
from ..utils.loggers import auth_logger

def get_employee(db: Session, employee_id: int):
    """Get employee by ID"""
    return db.query(tables.Employee).filter(tables.Employee.id == employee_id).first()

def get_employee_by_lastname(db: Session, last_name: str):
    """Get employee by last name"""
    return (
        db.query(tables.Employee)
        .filter(tables.Employee.last_name == last_name)
        .first()
    )

def create_employee(db: Session, employee: models.EmployeeCreate):
    """Create new employee"""
    try:
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
        
        auth_logger.info(
            "Employee created",
            extra={"employee_id": db_employee.id}
        )
        
        return db_employee
        
    except Exception as e:
        db.rollback()
        auth_logger.error(f"Error creating employee: {e}", exc_info=True)
        raise