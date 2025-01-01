"""Script to add a new employee to the database"""
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.crud import employees
from app.schemas.employee import EmployeeCreate
from app.utils.auth import get_password_hash

def add_employee():
    """Add a new employee to the database"""
    db = SessionLocal()
    try:
        # Create employee data
        employee = EmployeeCreate(
            first_name="Сотрудник",
            last_name="Лесников",
            department="general",
            office="101",
            password="111111"
        )
        
        # Check if employee already exists
        existing_employee = employees.get_employee_by_lastname(db, employee.last_name)
        if existing_employee:
            print(f"Сотрудник {employee.last_name} уже существует")
            return
        
        # Hash password before saving
        employee_dict = employee.model_dump()
        employee_dict["password"] = get_password_hash(employee_dict["password"])
        
        # Create new employee
        db_employee = employees.create_employee(db, employee_dict)
        print(f"Создан сотрудник: {db_employee.last_name} (ID: {db_employee.id})")
        
    except Exception as e:
        print(f"Ошибка при создании сотрудника: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_employee()