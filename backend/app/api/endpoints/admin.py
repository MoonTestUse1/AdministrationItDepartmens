"""Admin router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.request import Request
from app.core.auth import get_current_user
from app.schemas.request import RequestCreate, Request as RequestSchema
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get system statistics"""
    return statistics.get_request_statistics(db)

@router.get("/requests", response_model=List[Request])
def get_all_requests(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all requests"""
    return requests.get_requests(db)

@router.get("/requests/{request_id}", response_model=Request)
async def get_request_by_id(
    request_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получить заявку по ID (только для админа)
    """
    request = requests.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request