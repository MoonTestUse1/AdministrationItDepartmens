"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.request import Request, RequestStatus, RequestPriority
from ..schemas.request import RequestCreate, RequestResponse
from ..utils.telegram import send_notification

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
    
    # Отправляем уведомление в Telegram
    try:
        # Получаем данные сотрудника для уведомления
        employee = db_request.employee
        notification_data = {
            'id': db_request.id,
            'employee_first_name': employee.first_name,
            'employee_last_name': employee.last_name,
            'department': db_request.department,
            'office': employee.office,
            'request_type': db_request.request_type,
            'priority': db_request.priority,
            'description': db_request.description,
            'status': db_request.status,
            'created_at': db_request.created_at.isoformat()
        }
        send_notification(notification_data)
    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        print(f"Error sending notification: {e}")
    
    return db_request