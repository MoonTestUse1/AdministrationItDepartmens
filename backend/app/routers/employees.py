"""Employees router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import employees
from ..schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from ..utils.auth import get_current_admin
from ..utils.auth import get_password_hash

router = APIRouter()

@router.post("", response_model=Employee)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Создание нового сотрудника (только для админа)
    """
    # Хэшируем пароль
    hashed_password = get_password_hash(employee.password)
    
    # Создаем сотрудника
    db_employee = employees.create_employee(
        db=db,
        employee=employee,
        hashed_password=hashed_password
    )
    return db_employee

@router.get("", response_model=List[Employee])
def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получение списка всех сотрудников (только для админа)
    """
    employees_list = employees.get_employees(db, skip=skip, limit=limit)
    return employees_list

@router.get("/{employee_id}", response_model=Employee)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получение информации о сотруднике по ID (только для админа)
    """
    db_employee = employees.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Обновление информации о сотруднике (только для админа)
    """
    db_employee = employees.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    # Если указан новый пароль, хэшируем его
    if employee.password:
        employee.password = get_password_hash(employee.password)
        
    updated_employee = employees.update_employee(
        db=db,
        employee_id=employee_id,
        employee=employee
    )
    return updated_employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Удаление сотрудника (только для админа)
    """
    db_employee = employees.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees.delete_employee(db=db, employee_id=employee_id)
    return {"message": "Employee deleted successfully"}