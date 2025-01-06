"""Token CRUD operations"""
from sqlalchemy.orm import Session
from typing import Optional
from ..models.token import Token

def create_token(db: Session, token: str, employee_id: int) -> Token:
    """Create new token"""
    db_token = Token(token=token, employee_id=employee_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_token(db: Session, token: str) -> Optional[Token]:
    """Get token by value"""
    return db.query(Token).filter(Token.token == token).first()

def delete_token(db: Session, token: str) -> bool:
    """Delete token"""
    db_token = get_token(db, token)
    if db_token:
        db.delete(db_token)
        db.commit()
        return True
    return False

def delete_employee_tokens(db: Session, employee_id: int) -> bool:
    """Delete all tokens for an employee"""
    db.query(Token).filter(Token.employee_id == employee_id).delete()
    db.commit()
    return True 