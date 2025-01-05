"""Admin router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.request import Request
from app.core.auth import get_current_user
from app.schemas.request import RequestCreate, Request as RequestSchema, RequestUpdate
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/statistics")
def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system statistics"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Общая статистика
    total_requests = db.query(func.count(Request.id)).scalar()
    total_users = db.query(func.count(User.id)).filter(User.is_admin == False).scalar()

    # Статистика по статусам
    status_stats = db.query(
        Request.status,
        func.count(Request.id)
    ).group_by(Request.status).all()

    # Статистика за последние 7 дней
    week_ago = datetime.utcnow() - timedelta(days=7)
    daily_stats = db.query(
        func.date(Request.created_at),
        func.count(Request.id)
    ).filter(
        Request.created_at >= week_ago
    ).group_by(
        func.date(Request.created_at)
    ).all()

    return {
        "total_requests": total_requests,
        "total_users": total_users,
        "status_stats": {
            status: count for status, count in status_stats
        },
        "daily_stats": {
            date.strftime("%Y-%m-%d"): count
            for date, count in daily_stats
        }
    }

@router.get("/requests", response_model=List[RequestSchema])
def get_all_requests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all requests (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    requests = db.query(Request).offset(skip).limit(limit).all()
    return requests

@router.put("/requests/{request_id}/status", response_model=RequestSchema)
def update_request_status(
    request_id: int,
    request_update: RequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update request status (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = request_update.status
    db.commit()
    db.refresh(request)
    return request

@router.get("/users", response_model=List[UserSchema])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    users = db.query(User).filter(User.is_admin == False).offset(skip).limit(limit).all()
    return users