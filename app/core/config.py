from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application Settings
    app_name: str = "HRMS API"
    app_version: str = "1.0.0"
    
    # Database Settings
    database_url: str = "postgresql://postgres:0987654321@localhost:5432/hr"
    
    # CORS Settings
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    
    # File Upload Settings
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()