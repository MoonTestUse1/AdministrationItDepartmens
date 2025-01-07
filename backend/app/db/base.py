"""Import all models for Alembic autogenerate support"""
from app.db.base_class import Base  # noqa
from app.models.employee import Employee  # noqa
from app.models.request import Request  # noqa
from app.models.token import Token  # noqa

# Import all models for Alembic autogenerate support
__all__ = ["Base", "Employee", "Request", "Token"] 