"""Database initialization script that runs on container startup"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.crud import employees
from app.models.employee import EmployeeCreate

def init_db():
    db = SessionLocal()
    try:
        # Create default employee
        employee = EmployeeCreate(
            first_name="Сотрудник",
            last_name="Лесников",
            department="general",
            office="101",
            password="1111"
        )
        
        existing = employees.get_employee_by_lastname(db, employee.last_name)
        if not existing:
            employees.create_employee(db, employee)
            print("Default employee created successfully")
        else:
            print("Default employee already exists")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()