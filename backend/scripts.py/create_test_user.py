"""Script to create a test user in the database"""
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.crud import employees
from app.models.employee import EmployeeCreate

def create_test_employee():
    db = SessionLocal()
    try:
        # Create test employee data
        test_employee = EmployeeCreate(
            first_name="Иван",
            last_name="Иванов",
            department="general",
            office="101",
            password="test123"
        )
        
        # Check if employee already exists
        existing_employee = employees.get_employee_by_lastname(db, test_employee.last_name)
        if existing_employee:
            print(f"Employee {test_employee.last_name} already exists")
            return
        
        # Create new employee
        db_employee = employees.create_employee(db, test_employee)
        print(f"Created test employee: {db_employee.last_name} (ID: {db_employee.id})")
        
    except Exception as e:
        print(f"Error creating test employee: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    create_test_employee()