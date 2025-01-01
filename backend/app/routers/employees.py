"""Employee management routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from pydantic import BaseModel
from ..utils.loggers import auth_logger
from ..models.employee import Employee

router = APIRouter()

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    department: str
    office: str
    password: str

@router.get("/")
async def get_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    try:
        return db.query(Employee).all()
    except Exception as e:
        auth_logger.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении списка сотрудников")

@router.post("/")
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create new employee"""
    try:
        # Создаем запись в БД
        db_employee = Employee(
            first_name=employee.first_name,
            last_name=employee.last_name,
            department=employee.department,
            office=employee.office,
            password=employee.password  # В реальном приложении пароль нужно хешировать
        )
        
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        
        return db_employee
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Сотрудник с такими данными уже существует"
        )
    except Exception as e:
        db.rollback()
        auth_logger.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании сотрудника")