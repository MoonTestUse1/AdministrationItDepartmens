"""Script to add a new employee to the database"""
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.crud import employees
from app.models.employee import EmployeeCreate

def add_employee():
    db = SessionLocal()
    try:
        # Create employee data
        employee = EmployeeCreate(
            first_name="",  # Имя не указано в требованиях
            last_name="Лесников",
            department="general",  # Общий отдел
            office="101",
            password="1111"
        )
        
        # Check if employee already exists
        existing_employee = employees.get_employee_by_lastname(db, employee.last_name)
        if existing_employee:
            print(f"Сотрудник {employee.last_name} уже существует")
            return
        
        # Create new employee
        db_employee = employees.create_employee(db, employee)
        print(f"Создан сотрудник: {db_employee.last_name} (ID: {db_employee.id})")
        
    except Exception as e:
        print(f"Ошибка при создании сотрудника: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    add_employee()