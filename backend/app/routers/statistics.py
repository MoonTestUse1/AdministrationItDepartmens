"""Statistics router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import requests
from ..models.employee import Employee
from ..utils.auth import get_current_admin

router = APIRouter()

@router.get("/")
def get_statistics(
    db: Session = Depends(get_db),
    current_admin: Employee = Depends(get_current_admin)
):
    """Get request statistics (admin only)"""
    stats = requests.get_statistics(db)
    return {
        "total": stats["total"],
        "by_status": stats["by_status"]
    } 