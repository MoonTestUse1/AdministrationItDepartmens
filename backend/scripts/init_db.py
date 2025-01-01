"""Database initialization script"""
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.crud import employees
from app.schemas.employee import EmployeeCreate
from app.utils.auth import get_password_hash

def init_db():
    """Initialize database with default data"""
    db = SessionLocal()
    try:
        # Create default admin employee
        employee = EmployeeCreate(
            first_name="Admin",
            last_name="Admin",
            department="IT",
            office="101",
            password="admin66"
        )
        
        # Check if admin already exists
        existing_employee = employees.get_employee_by_lastname(db, employee.last_name)
        if existing_employee:
            print("Admin already exists")
            return
        
        # Hash password before saving
        employee_dict = employee.model_dump()
        employee_dict["password"] = get_password_hash(employee_dict["password"])
        
        # Create admin
        db_employee = employees.create_employee(db, employee_dict)
        print(f"Created admin employee with ID: {db_employee.id}")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()