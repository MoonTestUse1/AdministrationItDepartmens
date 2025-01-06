"""JWT utilities"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from ..core.config import settings
from ..models.token import Token
from ..schemas.auth import TokenData

def create_access_token(data: dict) -> str:
    """Create access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session) -> Optional[TokenData]:
    """Verify token"""
    try:
        # Проверяем, что токен действителен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        employee_id = int(payload.get("sub"))
        if employee_id is None:
            return None
        
        # Проверяем, что токен существует в базе
        db_token = db.query(Token).filter(Token.token == token).first()
        if not db_token:
            return None
            
        return TokenData(employee_id=employee_id)
    except (JWTError, ValueError):
        return None

def create_and_save_token(employee_id: int, db: Session) -> str:
    """Create and save token"""
    # Создаем токен
    access_token = create_access_token({"sub": str(employee_id)})
    
    # Сохраняем токен в базу
    db_token = Token(
        token=access_token,
        employee_id=employee_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    
    return access_token 