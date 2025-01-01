"""Employees router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    employees = db.query(Employee).all()
    return employees

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
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