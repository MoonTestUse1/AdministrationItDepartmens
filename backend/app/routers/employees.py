"""Employees router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from ..utils.auth import get_current_admin
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("", response_model=List[EmployeeResponse])
@router.get("/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db), _: dict = Depends(get_current_admin)):
    """Get all employees"""
    employees = db.query(Employee).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_admin)):
    """Get employee by ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee

@router.post("", response_model=EmployeeResponse)
@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_admin)):
    """Create new employee"""
    # Хешируем пароль
    hashed_password = pwd_context.hash(employee.password)
    
    # Создаем нового сотрудника
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        department=employee.department,
        office=employee.office,
        password=hashed_password
    )
    
    # Сохраняем в базу данных
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update employee data"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    
    # Обновляем данные
    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Delete employee"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    
    db.delete(db_employee)
    db.commit()
    return {"message": "Сотрудник успешно удален"}