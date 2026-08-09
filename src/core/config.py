import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CipherVista"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str
    
    # JWT Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        # This allows the app to run even if some variables are loaded from the OS instead of the .env file
        extra = "ignore"

settings = Settings()