"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..crud import requests
from ..schemas.request import Request, RequestCreate, RequestUpdate
from ..models.request import RequestStatus
from ..utils.auth import get_current_employee, get_current_admin

router = APIRouter()

@router.post("/", response_model=Request)
def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Create new request"""
    return requests.create_request(db, request, current_employee["id"])

@router.get("/my", response_model=List[Request])
def get_employee_requests(
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Get current employee's requests"""
    return requests.get_employee_requests(db, current_employee["id"])

@router.get("/admin", response_model=List[Request])
def get_all_requests(
    status: Optional[RequestStatus] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all requests (admin only)"""
    return requests.get_requests(db, status=status, skip=skip, limit=limit)

@router.patch("/{request_id}/status", response_model=Request)
def update_request_status(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update request status (admin only)"""
    db_request = requests.update_request_status(db, request_id, request_update.status)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.get("/statistics")
def get_request_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get request statistics (admin only)"""
    stats = requests.get_statistics(db)
    return {
        "total": stats["total"],
        "by_status": {
            status: count
            for status, count in stats["by_status"].items()
        }
    }