"""Request endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.request import Request
from app.schemas.request import RequestCreate, Request as RequestSchema
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=RequestSchema)
def create_request(
    request: RequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new request."""
    db_request = Request(
        employee_id=current_user.id,
        **request.model_dump()
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/my", response_model=List[RequestSchema])
def get_my_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's requests."""
    return db.query(Request).filter(Request.employee_id == current_user.id).all()

@router.get("/{request_id}", response_model=RequestSchema)
def get_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get request by ID."""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    if not current_user.is_admin and request.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this request")
    return request