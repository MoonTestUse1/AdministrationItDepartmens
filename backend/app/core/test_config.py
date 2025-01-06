"""Test configuration"""
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    """Test settings"""
    PROJECT_NAME: str = "Employee Request System Test"
    
    # Database
    DATABASE_URL: str = "sqlite:///:memory:"
    
    # JWT
    SECRET_KEY: str = "test_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    class Config:
        """Pydantic config"""
        case_sensitive = True

test_settings = TestSettings() 