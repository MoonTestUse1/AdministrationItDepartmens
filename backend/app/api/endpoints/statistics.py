"""Statistics router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import statistics
from ..utils.auth import get_current_admin

router = APIRouter()

@router.get("/")
def get_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get system statistics"""
    return statistics.get_request_statistics(db) 