"""Employee router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from ..database import get_db
from ..crud import employees
from ..schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from ..utils.auth import get_current_admin, get_password_hash

# Настройка логирования
logger = logging.getLogger(__name__)

router = APIRouter(tags=["employees"])

@router.post("", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Create new employee"""
    try:
        logger.info(f"Creating employee: {employee}")
        hashed_password = get_password_hash(employee.password)
        return employees.create_employee(db, employee, hashed_password)
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating employee"
        )

@router.get("", response_model=List[Employee])
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all employees"""
    try:
        logger.info("Getting all employees")
        return employees.get_employees(db, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error getting employees: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting employees"
        )

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get employee by ID"""
    try:
        logger.info(f"Getting employee by ID: {employee_id}")
        db_employee = employees.get_employee(db, employee_id)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting employee"
        )

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update employee data"""
    try:
        logger.info(f"Updating employee {employee_id}: {employee}")
        db_employee = employees.update_employee(db, employee_id, employee)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating employee"
        )

@router.delete("/{employee_id}", response_model=Employee)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Delete employee"""
    try:
        logger.info(f"Deleting employee: {employee_id}")
        db_employee = employees.delete_employee(db, employee_id)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting employee"
        )