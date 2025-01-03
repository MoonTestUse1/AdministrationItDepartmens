"""Statistics CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models.request import Request, RequestStatus

def get_request_statistics(db: Session):
    """Get request statistics"""
    # Общее количество заявок
    total_requests = db.query(func.count(Request.id)).scalar()

    # Количество заявок по статусам
    status_counts = {
        RequestStatus.NEW: 0,
        RequestStatus.IN_PROGRESS: 0,
        RequestStatus.COMPLETED: 0,
        RequestStatus.REJECTED: 0
    }

    # Получаем количество заявок для каждого статуса
    status_query = db.query(
        Request.status,
        func.count(Request.id)
    ).group_by(Request.status).all()

    for status, count in status_query:
        if status in status_counts:
            status_counts[status] = count

    # Статистика за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    recent_requests = db.query(func.count(Request.id)).filter(
        Request.created_at >= week_ago
    ).scalar()

    return {
        "total_requests": total_requests or 0,
        "by_status": status_counts,
        "recent_requests": recent_requests or 0
    }
