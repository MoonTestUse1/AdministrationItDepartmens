from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from redis import Redis
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.token import Token
from ..crud.employees import get_employee

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        employee_id: int = payload.get("sub")
        if employee_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
            
        # Проверяем токен в Redis
        if not redis.get(f"token:{token}"):
            # Если токена нет в Redis, проверяем в БД
            db_token = db.query(Token).filter(Token.access_token == token).first()
            if not db_token or db_token.expires_at < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired or is invalid",
                )
            # Если токен валиден, кэшируем его в Redis
            redis.setex(
                f"token:{token}",
                timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "valid"
            )
            
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def create_and_save_token(employee_id: int, db: Session) -> str:
    # Создаем JWT токен
    access_token = create_access_token({"sub": str(employee_id)})
    expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Сохраняем в БД
    db_token = Token(
        access_token=access_token,
        employee_id=employee_id,
        expires_at=expires_at
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
    employee = get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Employee not found",
        )
    return employee 