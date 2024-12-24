from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .models import employee as employee_models
from .models import request as request_models
from .schemas import tables
from .crud import employees, requests, auth, statistics
from .database import engine, get_db
from .models.request import StatusUpdate
from .bot.notifications import send_notification
from .bot import start_bot
import threading
import asyncio


tables.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_bot():
    asyncio.run(start_bot())


bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# CORS middleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth endpoints
@app.post("/api/test/create-user")
def create_test_user(db: Session = Depends(get_db)):
    test_user = employee_models.EmployeeCreate(
        first_name="Test",
        last_name="User",
        department="general",
        office="101",
        password="test123"
    )
    return employees.create_employee(db=db, employee=test_user)
@app.post("/api/auth/login")
def login(credentials: dict, db: Session = Depends(get_db)):
    print(f"Login attempt for: {credentials['lastName']}")  # Добавьте для отладки
    employee = auth.authenticate_employee(db, credentials["lastName"], credentials["password"])
    if not employee:
        raise HTTPException(
            status_code=401, 
            detail="Неверная фамилия или пароль"
        )
    return employee


@app.post("/api/auth/admin")
def admin_login(credentials: dict, db: Session = Depends(get_db)):
    if not auth.authenticate_admin(
        db, credentials["username"], credentials["password"]
    ):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    return {"success": True}


# Employee endpoints
@app.post("/api/employees/", response_model=employee_models.Employee)
def create_employee(
    employee: employee_models.EmployeeCreate, db: Session = Depends(get_db)
):
    db_employee = employees.get_employee_by_lastname(db, employee.last_name)
    if db_employee:
        raise HTTPException(status_code=400, detail="Last name already registered")
    return employees.create_employee(db=db, employee=employee)


@app.get("/api/employees/", response_model=List[employee_models.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return employees.get_employees(db, skip=skip, limit=limit)


@app.patch("/api/employees/{employee_id}")
def update_employee(employee_id: int, data: dict, db: Session = Depends(get_db)):
    return employees.update_employee(db, employee_id, data)


# Request endpoints
@app.post("/api/requests/")
def create_request(
    request: request_models.RequestCreate, db: Session = Depends(get_db)
):
    # Create request in database
    new_request = requests.create_request(db=db, request=request)

    # Get employee details for the notification
    employee = employees.get_employee(db, new_request.employee_id)

    # Prepare notification data
    notification_data = {
        "id": new_request.id,
        "employee_last_name": employee.last_name,
        "employee_first_name": employee.first_name,
        "department": new_request.department,
        "office": employee.office,
        "request_type": new_request.request_type,
        "priority": new_request.priority,
        "description": new_request.description,
        "created_at": new_request.created_at.isoformat(),
    }

    # Send notification to Telegram (non-blocking)
    try:
        send_notification(notification_data)
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

    return new_request


@app.patch("/api/requests/{request_id}/status")
def update_request_status(
    request_id: int,
    status_update: request_models.StatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        request = requests.update_request_status(db, request_id, status_update.status)
        if request is None:
            raise HTTPException(status_code=404, detail="Request not found")
        return request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/requests/", response_model=request_models.Request)
def create_request(request_data: dict, db: Session = Depends(get_db)):
    return requests.create_request(db=db, request_data=request_data)


@app.get("/api/requests/", response_model=List[request_models.RequestWithEmployee])
def read_requests(
    skip: int = 0,
    limit: int = 100,
    last_name: str = None,
    db: Session = Depends(get_db),
):
    if last_name:
        return requests.get_requests_by_employee_lastname(db, last_name)
    return requests.get_requests(db, skip=skip, limit=limit)


@app.patch("/api/requests/{request_id}/status")
def update_request_status(request_id: int, status: str, db: Session = Depends(get_db)):
    request = requests.update_request_status(db, request_id, status)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@app.patch("/api/requests/{request_id}/status")
def update_request_status(
    request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)
):
    try:
        request = requests.update_request_status(db, request_id, status_update.status)
        if request is None:
            raise HTTPException(status_code=404, detail="Request not found")
        return request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/statistics")
def get_statistics(period: str = "week", db: Session = Depends(get_db)):
    return statistics.get_statistics(db, period)
