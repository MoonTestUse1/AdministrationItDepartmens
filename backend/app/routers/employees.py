"""Employee management routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import employees as employees_crud
from ..models.employee import EmployeeCreate
from ..utils.loggers import auth_logger

router = APIRouter()

@router.post("/")
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create new employee"""
    try:
        db_employee = employees_crud.create_employee(db, employee)
        auth_logger.info(
            "Employee created",
            extra={"employee_id": db_employee.id}
        )
        return {
            "id": db_employee.id,
            "firstName": db_employee.first_name,
            "lastName": db_employee.last_name,
            "department": db_employee.department,
            "office": db_employee.office,
            "createdAt": db_employee.created_at
        }
    except Exception as e:
        auth_logger.error(f"Error creating employee: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при создании сотрудника")