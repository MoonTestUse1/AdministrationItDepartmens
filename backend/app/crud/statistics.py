"""Statistics CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from ..models.request import Request, RequestStatus

def get_statistics(db: Session, period: str = "week"):
    """Get statistics for the given period"""
    try:
        # Calculate date range
        end_date = datetime.now()
        if period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=7)  # default to week

        # Get total requests
        total_requests = db.query(func.count(Request.id)).scalar() or 0

        # Get requests by status
        requests_by_status = (
            db.query(Request.status, func.count(Request.id))
            .group_by(Request.status)
            .all()
        )

        # Convert to dictionary
        status_counts = {
            status.name: 0 for status in RequestStatus
        }
        for status, count in requests_by_status:
            status_counts[status.name] = count

        # Get recent requests
        recent_requests = (
            db.query(Request)
            .filter(Request.created_at >= start_date)
            .order_by(Request.created_at.desc())
            .limit(5)
            .all()
        )

        return {
            "total_requests": total_requests,
            "status_counts": status_counts,
            "recent_requests": recent_requests
        }

    except Exception as e:
        print(f"Error getting statistics: {e}")
        raise
