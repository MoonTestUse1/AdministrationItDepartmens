"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Для создания таблиц импортируем модели
from .models.employee import Employee  # noqa
from .models.request import Request  # noqa
from .models.token import Token  # noqa

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Для SQLite нужны специальные параметры подключения
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()