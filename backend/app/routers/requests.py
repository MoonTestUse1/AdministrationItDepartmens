"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..crud import requests
from ..schemas.request import Request, RequestCreate, RequestUpdate
from ..models.request import RequestStatus
from ..utils.auth import get_current_employee, get_current_admin
from ..utils.telegram import notify_new_request
from ..websockets.notifications import notification_manager

router = APIRouter()

@router.websocket("/ws/admin")
async def websocket_admin_endpoint(websocket: WebSocket):
    """WebSocket endpoint для админов"""
    await notification_manager.connect(websocket, "admin")
    try:
        while True:
            data = await websocket.receive_text()
            # Здесь можно добавить обработку сообщений от админа
    except WebSocketDisconnect:
        notification_manager.disconnect(websocket, "admin")

@router.websocket("/ws/employee/{employee_id}")
async def websocket_employee_endpoint(websocket: WebSocket, employee_id: int):
    """WebSocket endpoint для сотрудников"""
    await notification_manager.connect(websocket, "employee")
    try:
        while True:
            data = await websocket.receive_text()
            # Здесь можно добавить обработку сообщений от сотрудника
    except WebSocketDisconnect:
        notification_manager.disconnect(websocket, "employee")

@router.post("/", response_model=Request)
async def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Create new request"""
    db_request = requests.create_request(db, request, current_employee["id"])
    # Отправляем уведомление в Telegram
    await notify_new_request(db_request.id)
    
    # Получаем полные данные о заявке для отправки через WebSocket
    request_data = {
        "id": db_request.id,
        "description": db_request.description,
        "status": db_request.status.value,
        "priority": db_request.priority.value,
        "request_type": db_request.request_type,
        "department": db_request.department,
        "employee_id": current_employee["id"],
        "employee_name": current_employee.get("full_name", ""),
        "created_at": db_request.created_at.isoformat()
    }
    
    # Отправляем уведомление через WebSocket всем админам
    await notification_manager.broadcast_to_admins({
        "type": "new_request",
        "data": request_data
    })
    return db_request

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
async def update_request_status(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update request status (admin only)"""
    db_request = requests.update_request_status(db, request_id, request_update.status)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Отправляем уведомление через WebSocket
    await notification_manager.broadcast_to_admins({
        "type": "status_update",
        "data": {
            "id": request_id,
            "status": request_update.status
        }
    })
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