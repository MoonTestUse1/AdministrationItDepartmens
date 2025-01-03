"""Employee router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import employees
from ..schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from ..utils.auth import get_current_admin, get_password_hash

router = APIRouter()

@router.post("/", response_model=Employee)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Create new employee"""
    hashed_password = get_password_hash(employee.password)
    return employees.create_employee(db, employee, hashed_password)

@router.get("/", response_model=List[Employee])
def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all employees"""
    return employees.get_employees(db, skip=skip, limit=limit)

@router.get("/{employee_id}/", response_model=Employee)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get employee by ID"""
    db_employee = employees.get_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}/", response_model=Employee)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update employee data"""
    db_employee = employees.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{employee_id}/", response_model=Employee)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Delete employee"""
    db_employee = employees.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee