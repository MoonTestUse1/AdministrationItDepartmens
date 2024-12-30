"""Request handling routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import requests as requests_crud
from ..crud import employees as employees_crud
from ..models.request import RequestCreate
from ..bot.notifications import send_notification
from ..utils.loggers import request_logger

router = APIRouter()

@router.post("/")
async def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    """Create new request"""
    try:
        # Verify employee exists
        employee = employees_crud.get_employee(db, request.employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Сотрудник не найден"
            )

        db_request = requests_crud.create_request(db, request)
        request_logger.info(
            "Request created",
            extra={"request_id": db_request.id, "employee_id": request.employee_id}
        )
        
        request_details = requests_crud.get_request_details(db, db_request.id)
        await send_notification(request_details)
        
        return db_request
        
    except HTTPException:
        raise
    except Exception as e:
        request_logger.error(
            f"Error creating request: {e}",
            extra={"employee_id": request.employee_id}
        )
        raise HTTPException(status_code=500, detail="Ошибка при создании заявки")