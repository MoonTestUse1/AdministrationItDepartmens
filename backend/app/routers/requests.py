"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.request import Request, RequestStatus, RequestPriority
from ..schemas.request import RequestCreate, RequestResponse

router = APIRouter()

@router.get("/", response_model=List[RequestResponse])
def get_requests(db: Session = Depends(get_db)):
    """Get all requests"""
    requests = db.query(Request).all()
    return requests

@router.post("/", response_model=RequestResponse)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    """Create new request"""
    # Создаем новую заявку
    db_request = Request(
        employee_id=request.employee_id,
        department=request.department,
        request_type=request.request_type,
        priority=request.priority,
        description=request.description,
        status=RequestStatus.NEW
    )
    
    # Сохраняем в базу данных
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_request