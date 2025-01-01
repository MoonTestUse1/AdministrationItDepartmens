"""Employee routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..crud import employees as employees_crud
from ..schemas.employee import EmployeeCreate, Employee
from ..utils.auth import get_password_hash

router = APIRouter()

@router.get("/employees/", response_model=List[Employee])
def get_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    try:
        return employees_crud.get_employees(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении списка сотрудников: {str(e)}"
        )

@router.post("/employees/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create new employee"""
    try:
        # Check if employee already exists
        db_employee = employees_crud.get_employee_by_lastname(db, employee.last_name)
        if db_employee:
            raise HTTPException(
                status_code=400,
                detail="Сотрудник с такой фамилией уже существует"
            )

        # Hash password
        employee_dict = employee.model_dump()
        employee_dict["password"] = get_password_hash(employee_dict["password"])
        
        # Create employee
        return employees_crud.create_employee(db=db, employee_data=employee_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании сотрудника: {str(e)}"
        )