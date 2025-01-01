"""Request routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..crud import requests as requests_crud
from ..schemas.request import RequestCreate, Request, RequestWithEmployee
from ..models.request import RequestStatus

router = APIRouter()

@router.post("/requests/", response_model=Request)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    """Create new request"""
    return requests_crud.create_request(db=db, request=request)

@router.get("/requests/{request_id}", response_model=RequestWithEmployee)
def get_request(request_id: int, db: Session = Depends(get_db)):
    """Get request by ID"""
    request = requests_crud.get_request_details(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request