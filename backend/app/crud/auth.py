from sqlalchemy.orm import Session
from ..schemas import tables
from ..utils.auth import verify_password


def authenticate_employee(db: Session, last_name: str, password: str):
    employee = db.query(tables.Employee).filter(tables.Employee.last_name == last_name).first()
    if not employee:
        return None
    if not verify_password(password, employee.password):
        return None
    return {
        "id": employee.id,
        "firstName": employee.first_name,
        "lastName": employee.last_name,
        "department": employee.department,
        "office": employee.office,
        "createdAt": employee.created_at
    }


def authenticate_admin(db: Session, username: str, password: str):
    # Здесь можно добавить логику для админа, пока используем хардкод
    if username == "admin" and password == "admin66":
        return True
    return False
