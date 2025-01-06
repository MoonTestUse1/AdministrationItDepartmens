"""Test configuration"""
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    """Test settings"""
    PROJECT_NAME: str = "Employee Request System Test"
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "test_app"
    
    # JWT
    SECRET_KEY: str = "test_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1
    
    # Testing
    TESTING: bool = True
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env.test",
        "extra": "allow"
    }

    def get_database_url(self) -> str:
        """Get database URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

test_settings = TestSettings() 