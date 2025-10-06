"""
Configuration settings for the OptimumBus API

This module handles all configuration settings using Pydantic Settings,
which automatically loads environment variables and provides type validation.
"""

from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    All settings can be overridden by setting corresponding environment variables.
    For example, DATABASE_URL=postgresql://... will override the default.
    """
    
    # Application Configuration
    APP_NAME: str = "OptimumBus API"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/optimumbus_db"
    POSTGRES_USER: str = "username"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "optimumbus_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """
        Parse CORS origins from comma-separated string or list
        
        This allows us to set ALLOWED_ORIGINS as either:
        - A comma-separated string: "http://localhost:3000,http://localhost:3001"
        - A JSON list: ["http://localhost:3000", "http://localhost:3001"]
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        """
        Pydantic configuration
        
        env_file: Load settings from .env file
        case_sensitive: Environment variable names are case-sensitive
        """
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
