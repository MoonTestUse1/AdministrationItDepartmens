"""Database connection check script"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def check_database_connection(database_url: str) -> bool:
    """Check database connection"""
    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Successfully connected to {database_url}")
            return True
    except SQLAlchemyError as error:
        print(f"Error connecting to {database_url}: {error}")
        return False

if __name__ == "__main__":
    # URL для основной базы данных
    main_db_url = "postgresql://postgres:postgres@localhost:5432/app"
    # URL для тестовой базы данных
    test_db_url = "postgresql://postgres:postgres@localhost:5432/test_app"

    main_ok = check_database_connection(main_db_url)
    test_ok = check_database_connection(test_db_url)

    if not (main_ok and test_ok):
        sys.exit(1)
    
    print("All database connections are successful!") 