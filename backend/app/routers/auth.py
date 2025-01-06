"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..crud import employees
from ..schemas.auth import Token, LoginCredentials
from ..utils.auth import verify_password
from ..utils.jwt import create_and_save_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Авторизация сотрудника"""
    # Разделяем username на имя и фамилию
    try:
        first_name, last_name = form_data.username.split()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username should be in format: 'First Last'",
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

@router.post("/admin/login", response_model=Token)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Авторизация администратора"""
    # Разделяем username на имя и фамилию
    try:
        first_name, last_name = form_data.username.split()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username should be in format: 'First Last'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем учетные данные администратора
    employee = employees.get_employee_by_credentials(db, first_name, last_name)
    if not employee or not employee.is_admin or not verify_password(form_data.password, employee.hashed_password):
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

