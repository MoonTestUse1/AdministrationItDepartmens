"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..crud import employees
from ..schemas.token import Token
from ..utils.security import verify_password
from ..utils.jwt import create_and_save_token
from ..dependencies import get_db

router = APIRouter()

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"

@router.post("/admin/login", response_model=Token)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Авторизация администратора"""
    # Проверяем фиксированные учетные данные администратора
    if form_data.username != ADMIN_LOGIN or form_data.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Получаем или создаем админа в базе
    admin = employees.get_employee_by_login(db, ADMIN_LOGIN)
    if not admin:
        # Если админа нет в базе, создаем его
        admin = employees.create_employee(db, {
            "login": ADMIN_LOGIN,
            "first_name": "Admin",
            "last_name": "User",
            "department": "IT",
            "office": "Main",
            "password": ADMIN_PASSWORD,
            "is_admin": True
        })
    
    # Создаем и сохраняем токен
    access_token = create_and_save_token(admin.id, db)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Авторизация сотрудника"""
    # Разделяем username на имя и фамилию
    try:
        first_name, last_name = form_data.username.split()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be in format: 'First Last'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем учетные данные сотрудника
    employee = employees.get_employee_by_credentials(db, first_name, last_name)
    if not employee or not verify_password(form_data.password, employee.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем и сохраняем токен
    access_token = create_and_save_token(employee.id, db)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

