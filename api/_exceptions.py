"""
RentCast API exceptions.

This module defines custom exceptions for the RentCast API client.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import ValidationError


class RentCastError(Exception):
    """Base exception for all RentCast API errors."""

    def __init__(
        self,
        message: str = "An error occurred with the RentCast API",
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        self.extra = kwargs
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"{self.status_code}: {self.message}"
        return self.message


class RentCastAPIError(RentCastError):
    """Raised when the RentCast API returns an error response."""

    def __init__(
        self,
        message: str = "API request failed",
        status_code: int | None = None,
        response: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(message, status_code, response, **kwargs)


class RentCastAuthenticationError(RentCastError):
    """Raised when authentication with the RentCast API fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = 401,
        response: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(message, status_code, response, **kwargs)


class RentCastRateLimitError(RentCastError):
    """Raised when the rate limit for the RentCast API is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        retry_after: int | None = None,
        response: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        self.retry_after = retry_after
        if retry_after:
            message = f"{message}. Please try again in {retry_after} seconds."
        super().__init__(message, status_code, response, **kwargs)


class RentCastValidationError(RentCastError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: list[dict[str, Any]] | list[ValidationError] | None = None,
        status_code: int = 400,
        response: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        self.errors = errors or []
        super().__init__(message, status_code, response, **kwargs)
        self.extra["errors"] = self.errors

    def __str__(self) -> str:
        error_messages = []
        for error in self.errors:
            if isinstance(error, ValidationError):
                error_messages.extend(err["msg"] for err in error.errors())
            else:
                error_messages.append(str(error))
        return f"{self.message}: {', '.join(error_messages)}"


class RentCastConnectionError(RentCastError):
    """Raised when a connection to the RentCast API cannot be established."""

    def __init__(
        self,
        message: str = "Failed to connect to RentCast API",
        **kwargs,
    ) -> None:
        super().__init__(message, **kwargs)


class RentCastTimeoutError(RentCastError):
    """Raised when a request to the RentCast API times out."""

    def __init__(
        self,
        message: str = "Request to RentCast API timed out",
        **kwargs,
    ) -> None:
        super().__init__(message, **kwargs)


class RentCastNotFoundError(RentCastError):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "The requested resource was not found",
        status_code: int = 404,
        response: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(message, status_code, response, **kwargs)