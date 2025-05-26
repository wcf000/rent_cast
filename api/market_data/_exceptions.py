"""
Market Data API Exceptions.

This module contains custom exceptions for the Market Data API client.
"""

class MarketDataError(Exception):
    """Base exception for market data related errors."""
    pass

class InvalidRequestError(MarketDataError):
    """Raised when the market data request is invalid."""
    pass

class DataNotAvailableError(MarketDataError):
    """Raised when the requested market data is not available."""
    pass