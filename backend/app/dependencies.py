"""Dependencies module"""
from typing import Generator, Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .database import SessionLocal
from .core.config import settings
from .utils.jwt import verify_token_in_db
from .models.employee import Employee

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_employee(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Employee:
    """Get current employee"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    token_data = verify_token_in_db(token, db)
    if not token_data:
        raise credentials_exception
    
    # Get employee
    employee = db.query(Employee).filter(Employee.id == token_data.employee_id).first()
    if not employee:
        raise credentials_exception
    
    return employee

async def get_current_active_employee(
    current_employee: Annotated[Employee, Depends(get_current_employee)]
) -> Employee:
    """Get current active employee"""
    if not current_employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive employee"
        )
    return current_employee

async def get_current_admin(
    current_employee: Annotated[Employee, Depends(get_current_employee)]
) -> Employee:
    """Get current admin"""
    if not current_employee.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The employee doesn't have enough privileges"
        )
    return current_employee 