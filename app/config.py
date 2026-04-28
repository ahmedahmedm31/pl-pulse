"""Application configuration."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "sqlite:///./plpulse.db"

    # Application
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Scraping
    SCRAPE_RATE_LIMIT: float = 2.0
    USER_AGENT: str = "PLPulse/1.0 (contact@plpulse.com)"

    # ML
    MODEL_PATH: str = "ml/saved_models/"
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.6

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
