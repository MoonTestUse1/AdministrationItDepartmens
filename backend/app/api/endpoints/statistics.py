"""Statistics router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.core.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.request import Request

router = APIRouter()

@router.get("/")
def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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