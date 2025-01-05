"""JWT utilities"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from redis import Redis
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.token import Token
from ..crud.employees import get_employee

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
            
        # Проверяем токен в Redis
        if not redis.get(f"token:{token}"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
            
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def create_and_save_token(user_id: int, db: Session) -> str:
    # Создаем JWT токен
    access_token = create_access_token({"sub": str(user_id)})
    
    # Сохраняем в БД
    db_token = Token(
        token=access_token,
        user_id=user_id
    )
    db.add(db_token)
    db.commit()
    
    # Кэшируем в Redis
    redis.setex(
        f"token:{access_token}",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "valid"
    )
    
    return access_token

def get_current_employee(token: str, db: Session):
    payload = verify_token(token, db)
    employee_id = int(payload.get("sub"))
    if employee_id == -1:  # Для админа
        return {"is_admin": True}
    employee = get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Employee not found",
        )
    return employee 