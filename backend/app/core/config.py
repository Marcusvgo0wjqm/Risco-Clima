from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Informações da app
    APP_NAME: str = "Clima Risk Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://clima_user:clima_password@localhost:5432/clima_risk_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Segurança
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    
    # APIs Externas
    NOAA_API_URL: str = "https://www.ncei.noaa.gov/products/weather-global-grid-observations"
    OPENWEATHER_API_KEY: Optional[str] = None
    ECMWF_API_KEY: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
