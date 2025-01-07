"""JWT utilities"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from ..core.config import settings
from ..core.test_config import test_settings
from ..models.token import Token
from ..schemas.auth import TokenData

def get_settings():
    """Get settings based on environment"""
    return test_settings if test_settings.TESTING else settings

def create_access_token(data: dict) -> str:
    """Create access token"""
    to_encode = data.copy()
    config = get_settings()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    """Verify token and return employee_id"""
    try:
        config = get_settings()
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        employee_id = int(payload.get("sub"))
        if employee_id is None:
            return None
        return employee_id
    except (JWTError, ValueError):
        return None

def verify_token_in_db(token: str, db: Session) -> Optional[TokenData]:
    """Verify token in database"""
    employee_id = verify_token(token)
    if employee_id is None:
        return None
        
    # Проверяем, что токен существует в базе
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token:
        return None
        
    return TokenData(employee_id=employee_id)

def create_and_save_token(employee_id: int, db: Session) -> str:
    """Create and save token"""
    # Создаем токен
    access_token = create_access_token({"sub": str(employee_id)})
    
    # Удаляем старые токены пользователя
    db.query(Token).filter(Token.employee_id == employee_id).delete()
    
    # Сохраняем новый токен в базу
    db_token = Token(
        token=access_token,
        employee_id=employee_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    
    return access_token 