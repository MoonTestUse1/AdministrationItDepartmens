"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.employee import Employee
from ..schemas.auth import AdminLogin, EmployeeLogin
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/admin/login")
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    if login_data.username == "admin" and login_data.password == "admin123":
        return {
            "access_token": "admin_token",
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/login")
def employee_login(login_data: EmployeeLogin, db: Session = Depends(get_db)):
    """Employee login endpoint"""
    # Ищем сотрудника по фамилии
    employee = db.query(Employee).filter(Employee.last_name == login_data.last_name).first()
    
    if not employee:
        raise HTTPException(
            status_code=401,
            detail="Сотрудник с такой фамилией не найден"
        )
    
    # Проверяем пароль
    if not pwd_context.verify(login_data.password, employee.password):
        raise HTTPException(
            status_code=401,
            detail="Неверный пароль"
        )
    
    # Возвращаем данные сотрудника
    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "department": employee.department,
        "office": employee.office,
        "access_token": f"employee_token_{employee.id}",  # Добавляем токен для авторизации
        "token_type": "bearer"
    }