"""Basic tests for PL Pulse application."""
import pytest
from app.config import settings


def test_settings():
    """Test that settings are loaded correctly."""
    assert settings.SECRET_KEY is not None
    assert settings.DATABASE_URL is not None


def test_app_version():
    """Test that app version is defined."""
    from app import __version__
    assert __version__ == "1.0.0"
