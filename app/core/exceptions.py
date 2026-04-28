"""Custom exceptions for the application."""


class PLPulseError(Exception):
    """Base exception for PL Pulse application."""

    pass


class ScrapingError(PLPulseError):
    """Exception raised when scraping fails."""

    pass


class DataValidationError(PLPulseError):
    """Exception raised when data validation fails."""

    pass


class PredictionError(PLPulseError):
    """Exception raised when prediction fails."""

    pass


class ResourceNotFoundError(PLPulseError):
    """Exception raised when a resource is not found."""

    pass
