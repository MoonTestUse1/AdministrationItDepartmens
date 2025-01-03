"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..crud import requests
from ..schemas.request import Request, RequestCreate, RequestUpdate, RequestStatistics
from ..utils.auth import get_current_employee, get_current_admin
from ..utils.telegram import notify_new_request

router = APIRouter()

@router.post("", response_model=Request)
async def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """
    Создание новой заявки
    """
    db_request = requests.create_request(db=db, request=request, employee_id=current_employee.id)
    await notify_new_request(db_request.id)
    return db_request

@router.get("", response_model=List[Request])
def get_employee_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """
    Получение списка заявок текущего сотрудника
    """
    return requests.get_employee_requests(db, employee_id=current_employee.id, skip=skip, limit=limit)

@router.get("/statistics", response_model=RequestStatistics)
def get_request_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Получение статистики по заявкам (только для админа)
    """
    return requests.get_statistics(db)

@router.put("/{request_id}", response_model=Request)
def update_request(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Обновление статуса заявки (только для админа)
    """
    db_request = requests.get_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return requests.update_request(db=db, request_id=request_id, request_update=request_update)

@router.delete("/{request_id}")
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """
    Удаление заявки (только для админа)
    """
    db_request = requests.get_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    requests.delete_request(db=db, request_id=request_id)
    return {"message": "Request deleted successfully"}