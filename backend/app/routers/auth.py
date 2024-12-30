"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import auth as auth_crud
from ..utils.loggers import auth_logger

router = APIRouter()

@router.post("/login")
async def login(credentials: dict, db: Session = Depends(get_db)):
    """Employee login endpoint"""
    try:
        # Validate required fields
        if not credentials.get("lastName") or not credentials.get("password"):
            raise HTTPException(
                status_code=400,
                detail="Необходимо указать фамилию и пароль"
            )

        employee = auth_crud.authenticate_employee(
            db, 
            credentials["lastName"], 
            credentials["password"]
        )
        
        if not employee:
            raise HTTPException(
                status_code=401,
                detail="Неверные учетные данные"
            )
            
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        auth_logger.error(f"Login error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка сервера")