from sqlalchemy import func, text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..schemas import tables
from ..models.request import RequestStatus


def get_statistics(db: Session, period: str = "week"):
    # Calculate date range based on period
    now = datetime.now()
    if period == "day":
        start_date = now - timedelta(days=1)
    elif period == "week":
        start_date = now - timedelta(weeks=1)
    elif period == "month":
        start_date = now - timedelta(days=30)
    else:  # all time
        start_date = datetime.min

    # Total requests
    total_requests = db.query(func.count(tables.Request.id)).scalar() or 0

    # Resolved requests in period
    resolved_requests = (
        db.query(func.count(tables.Request.id))
        .filter(tables.Request.status == RequestStatus.RESOLVED)
        .filter(tables.Request.created_at >= start_date)
        .scalar()
        or 0
    )

    # Average resolution time (in hours)
    avg_resolution = (
        db.query(
            func.avg(func.julianday("now") - func.julianday(tables.Request.created_at))
            * 24
        )
        .filter(
            tables.Request.status == RequestStatus.RESOLVED,
            tables.Request.created_at >= start_date,
        )
        .scalar()
    )

    avg_resolution_time = f"{int(avg_resolution or 0)}ч" if avg_resolution else "0ч"

    # Request volume over time
    volume_data = (
        db.query(
            func.date(tables.Request.created_at).label("date"),
            func.count(tables.Request.id).label("count"),
        )
        .filter(tables.Request.created_at >= start_date)
        .group_by(text("date"))
        .all()
    )

    # Request types distribution
    type_distribution = (
        db.query(tables.Request.request_type, func.count(tables.Request.id))
        .group_by(tables.Request.request_type)
        .all()
    )

    # Status distribution
    status_distribution = (
        db.query(tables.Request.status, func.count(tables.Request.id))
        .group_by(tables.Request.status)
        .all()
    )

    # Ensure all statuses are represented
    all_statuses = {status.value: 0 for status in RequestStatus}
    for status, count in status_distribution:
        all_statuses[status] = count

    status_data = [(status, count) for status, count in all_statuses.items()]

    return {
        "totalRequests": total_requests,
        "resolvedRequests": resolved_requests,
        "averageResolutionTime": avg_resolution_time,
        "volumeLabels": [str(d[0]) for d in volume_data],
        "volumeData": [d[1] for d in volume_data],
        "typeLabels": [t[0] for t in type_distribution],
        "typeData": [t[1] for t in type_distribution],
        "statusLabels": [s[0] for s in status_data],
        "statusData": [s[1] for s in status_data],
    }
