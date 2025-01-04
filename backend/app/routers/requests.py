"""Requests router"""
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from ..database import get_db
from ..crud import requests
from ..schemas.request import Request, RequestCreate, RequestUpdate
from ..models.request import RequestStatus
from ..utils.auth import get_current_employee, get_current_admin
from ..utils.telegram import notify_new_request
from ..websockets.notifications import notification_manager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/admin")
async def websocket_admin_endpoint(websocket: WebSocket):
    """WebSocket endpoint для админов"""
    logger.info("Admin WebSocket connection attempt")
    await notification_manager.connect(websocket, "admin")
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message from admin: {data}")
            
            if data.get("type") == "ping":
                await notification_manager.handle_ping(websocket)
    except WebSocketDisconnect:
        logger.info("Admin WebSocket disconnected")
        notification_manager.disconnect(websocket, "admin")
    except Exception as e:
        logger.error(f"Error in admin websocket: {e}")
        notification_manager.disconnect(websocket, "admin")

@router.websocket("/ws/employee/{employee_id}")
async def websocket_employee_endpoint(websocket: WebSocket, employee_id: int):
    """WebSocket endpoint для сотрудников"""
    logger.info(f"Employee {employee_id} WebSocket connection attempt")
    await notification_manager.connect(websocket, "employee")
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message from employee {employee_id}: {data}")
            
            if data.get("type") == "ping":
                await notification_manager.handle_ping(websocket)
    except WebSocketDisconnect:
        logger.info(f"Employee {employee_id} WebSocket disconnected")
        notification_manager.disconnect(websocket, "employee")
    except Exception as e:
        logger.error(f"Error in employee websocket: {e}")
        notification_manager.disconnect(websocket, "employee")

@router.post("/", response_model=Request)
async def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_employee: dict = Depends(get_current_employee)
):
    """Create new request"""
    logger.info(f"Creating new request from employee {current_employee['id']}")
    db_request = requests.create_request(db, request, current_employee["id"])
    
    # Отправляем уведомление в Telegram
    await notify_new_request(db_request.id)
    
    # Получаем актуальную статистику
    stats = requests.get_statistics(db)
    logger.info(f"Current statistics after new request: {stats}")
    
    # Получаем полные данные о заявке для отправки через WebSocket
    request_data = {
        "id": db_request.id,
        "description": db_request.description,
        "status": db_request.status.value.lower(),
        "priority": db_request.priority.value.lower(),
        "request_type": db_request.request_type,
        "department": db_request.department,
        "employee_id": current_employee["id"],
        "employee_name": current_employee.get("full_name", ""),
        "created_at": db_request.created_at.isoformat()
    }
    
    # Формируем сообщение для WebSocket
    ws_message = {
        "type": "new_request",
        "data": request_data,
        "statistics": stats
    }
    
    logger.info(f"Broadcasting WebSocket message for new request: {ws_message}")
    # Отправляем уведомление через WebSocket всем админам
    await notification_manager.broadcast_to_admins(ws_message)
    
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
    logger.info(f"Updating request {request_id} status to {request_update.status}")
    db_request = requests.update_request_status(db, request_id, request_update.status)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Получаем актуальную статистику
    stats = requests.get_statistics(db)
    logger.info(f"Current statistics after status update: {stats}")
    
    # Формируем сообщение для WebSocket
    ws_message = {
        "type": "status_update",
        "data": {
            "id": request_id,
            "status": db_request.status.value.lower()
        },
        "statistics": stats
    }
    
    logger.info(f"Broadcasting WebSocket message for status update: {ws_message}")
    # Отправляем уведомление через WebSocket
    await notification_manager.broadcast_to_admins(ws_message)
    
    return db_request

@router.get("/statistics")
def get_request_statistics(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get request statistics (admin only)"""
    stats = requests.get_statistics(db)
    logger.info(f"Returning statistics: {stats}")
    return stats