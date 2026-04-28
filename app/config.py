from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "TCS Wings Data Engineering Prep"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tcs_wings.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tcs-wings-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

settings = Settings()