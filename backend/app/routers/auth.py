"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..crud import employees
from ..schemas.auth import Token
from ..utils.auth import verify_password
from ..utils.jwt import create_and_save_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Проверяем учетные данные сотрудника
    employee = employees.get_employee_by_last_name(db, form_data.username)
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

@router.post("/admin/token", response_model=Token)
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Проверяем учетные данные администратора
    if form_data.username != "admin" or form_data.password != "admin123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Для админа используем специальный ID
    admin_id = -1
    access_token = create_and_save_token(admin_id, db)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }