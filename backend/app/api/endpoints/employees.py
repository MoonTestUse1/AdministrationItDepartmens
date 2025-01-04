"""Employee router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user, get_password_hash
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_employee(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Проверяем, не существует ли уже пользователь с таким email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserSchema])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    users = db.query(User).filter(User.is_admin == False).offset(skip).limit(limit).all()
    return users