"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import auth as auth_crud
from ..schemas.auth import AdminLogin

router = APIRouter()

@router.post("/admin")
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    if login_data.username == "admin" and login_data.password == "admin123":
        return {"access_token": "admin_token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")