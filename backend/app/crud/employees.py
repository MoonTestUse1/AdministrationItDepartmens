"""Employee CRUD operations"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from ..models.employee import Employee
from ..utils.security import get_password_hash

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """Get employee by ID"""
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_credentials(db: Session, first_name: str, last_name: str) -> Optional[Employee]:
    """Get employee by first name and last name"""
    return db.query(Employee).filter(
        Employee.first_name == first_name,
        Employee.last_name == last_name
    ).first()

def get_employee_by_login(db: Session, login: str) -> Optional[Employee]:
    """Get employee by login"""
    return db.query(Employee).filter(Employee.login == login).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    """Get list of employees"""
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee_data: Dict[str, Any]) -> Employee:
    """Create new employee"""
    # Хешируем пароль
    hashed_password = get_password_hash(employee_data["password"])
    
    # Создаем сотрудника
    db_employee = Employee(
        login=employee_data.get("login"),
        first_name=employee_data["first_name"],
        last_name=employee_data["last_name"],
        department=employee_data["department"],
        office=employee_data["office"],
        hashed_password=hashed_password,
        is_admin=employee_data.get("is_admin", False)
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee: Employee, employee_data: Dict[str, Any]) -> Employee:
    """Update employee"""
    # Если есть пароль в данных, хешируем его
    if "password" in employee_data:
        employee_data["hashed_password"] = get_password_hash(employee_data.pop("password"))
    
    # Обновляем поля
    for field, value in employee_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee: Employee) -> None:
    """Delete employee"""
    db.delete(employee)
    db.commit()