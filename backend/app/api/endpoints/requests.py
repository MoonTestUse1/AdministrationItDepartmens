"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.request import Request
from app.schemas.request import RequestCreate, Request as RequestSchema

router = APIRouter()

@router.post("/", response_model=RequestSchema)
def create_request(
    request: RequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new request"""
    db_request = Request(
        **request.dict(),
        employee_id=current_user.id,
        status="new"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/", response_model=List[RequestSchema])
def read_requests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all requests (admin only)"""
    if current_user.is_admin:
        requests = db.query(Request).offset(skip).limit(limit).all()
    else:
        requests = db.query(Request).filter(
            Request.employee_id == current_user.id
        ).offset(skip).limit(limit).all()
    return requests

@router.get("/{request_id}", response_model=RequestSchema)
def read_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific request"""
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Проверяем права доступа
    if not current_user.is_admin and request.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return request

@router.put("/{request_id}", response_model=RequestSchema)
def update_request(
    request_id: int,
    request_update: RequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a request"""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Проверяем права доступа
    if not current_user.is_admin and db_request.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Обновляем заявку
    for key, value in request_update.dict().items():
        setattr(db_request, key, value)
    
    db.commit()
    db.refresh(db_request)
    return db_request

@router.delete("/{request_id}", response_model=RequestSchema)
def delete_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a request"""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Только админ может удалять заявки
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_request)
    db.commit()
    return db_request