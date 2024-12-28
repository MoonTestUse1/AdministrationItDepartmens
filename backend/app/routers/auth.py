"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import auth as auth_crud
from ..models.employee import EmployeeBase
from logging import getLogger

router = APIRouter()
logger = getLogger(__name__)

@router.post("/login")
async def login(credentials: dict, db: Session = Depends(get_db)):
    """Employee login endpoint"""
    try:
        employee = auth_crud.authenticate_employee(
            db, 
            credentials.get("lastName"), 
            credentials.get("password")
        )
        if not employee:
            raise HTTPException(status_code=401, detail="Неверные учетные данные")
        return employee
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка сервера")

@router.post("/admin")
async def admin_login(credentials: dict, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    try:
        is_valid = auth_crud.authenticate_admin(
            db,
            credentials.get("username"),
            credentials.get("password")
        )
        if not is_valid:
            raise HTTPException(status_code=401, detail="Неверные учетные данные")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Admin login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка сервера")