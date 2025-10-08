"""
RentCast API Client.

This module provides the main client class for interacting with the RentCast API.
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from .api._exceptions import (
    RentCastAPIError,
    RentCastAuthenticationError,
    RentCastError,
    RentCastRateLimitError,
    RentCastValidationError,
)
from .api.listings.rental_listings import RentalListingsClient
from .api.listings.rental_listing_by_id import RentalListingByIdClient
from .api.listings.sale import SaleListingsClient
from .api.listings.sale_by_id import SaleListingByIdClient
from .api.market_data.statistics import MarketDataClient
from .api.property_data.random_records import RandomPropertyClient
from .api.property_data.record_by_id import PropertyRecordClient
from .api.property_data.records import PropertiesClient
from .api.valuation.rent_estimate import RentEstimateClient
from .api.valuation.valuation import PropertyValuationClient
from .config import RentCastConfig

logger = logging.getLogger(__name__)


class RentCastClient:
    """
    Main client for interacting with the RentCast API.

    This client handles authentication, request/response processing, and error handling
    for all RentCast API endpoints.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.rentcast.io/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
        **kwargs,
    ):
        """
        Initialize the RentCast API client.

        Args:
            api_key: Your RentCast API key. If not provided, will be loaded from
                environment variables or config.
            base_url: Base URL for the RentCast API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            **kwargs: Additional arguments to pass to the HTTP client.
        """
        self.config = RentCastConfig()
        self.api_key = api_key or self.config.api_key
        if not self.api_key:
            raise RentCastAuthenticationError("No API key provided and none found in config")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = None
        
        # Initialize client instances
        self._property_data = None
        self._property_record = None
        self._random_properties = None
        self._market_data = None
        self._rental_listings = None
        self._rental_listing = None
        self._sale_listings = None
        self._sale_listing = None
        self._property_valuation = None
        self._rent_estimate = None

        # Configure HTTP client
        self.client_params = {
            "base_url": self.base_url,
            "timeout": timeout,
            "headers": {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            **kwargs,
        }

    async def __aenter__(self) -> RentCastClient:
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()

    async def start(self) -> None:
        """Initialize the HTTP client session."""
        if self._client is None:
            self._client = httpx.AsyncClient(**self.client_params)

    @property
    def property_data(self) -> PropertiesClient:
        """Access the properties API client."""
        if self._property_data is None:
            self._property_data = PropertiesClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._property_data

    @property
    def property_record(self) -> PropertyRecordClient:
        """Access the property record by ID API client."""
        if self._property_record is None:
            self._property_record = PropertyRecordClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._property_record

    @property
    def random_properties(self) -> RandomPropertyClient:
        """Access the random properties API client."""
        if self._random_properties is None:
            self._random_properties = RandomPropertyClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._random_properties

    @property
    def market_data(self) -> MarketDataClient:
        """Access the market data API client."""
        if self._market_data is None:
            self._market_data = MarketDataClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._market_data
        
    @property
    def valuation(self) -> PropertyValuationClient:
        """Access the property valuation API client."""
        if self._property_valuation is None:
            self._property_valuation = PropertyValuationClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._property_valuation
        
    @property
    def rent_estimate(self) -> RentEstimateClient:
        """Access the rent estimate API client."""
        if self._rent_estimate is None:
            self._rent_estimate = RentEstimateClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries
            )
        return self._rent_estimate

class ListingsClient:
    """Client for accessing listing-related endpoints."""

    def __init__(self, client: RentCastClient) -> None:
        self._client = client

    @property
    def listings(self) -> ListingsClient:
        """Access the listings API clients."""
        class ListingsClient:
            def __init__(self, client: RentCastClient) -> None:
                self._client = client

            @property
            def rental(self) -> RentalListingsClient:
                """Access the rental listings client."""
                if self._client._rental_listings is None:
                    self._client._rental_listings = RentalListingsClient(
                        api_key=self._client.api_key,
                        base_url=self._client.base_url,
                        timeout=self._client.timeout,
                        max_retries=self._client.max_retries
                    )
                return self._client._rental_listings

            @property
            def rental_by_id(self) -> RentalListingByIdClient:
                """Access the rental listing by ID client."""
                if self._client._rental_listing is None:
                    self._client._rental_listing = RentalListingByIdClient(
                        api_key=self._client.api_key,
                        base_url=self._client.base_url,
                        timeout=self._client.timeout,
                        max_retries=self._client.max_retries
                    )
                return self._client._rental_listing

            @property
            def sale(self) -> SaleListingsClient:
                """Access the sale listings client."""
                if self._client._sale_listings is None:
                    self._client._sale_listings = SaleListingsClient(
                        api_key=self._client.api_key,
                        base_url=self._client.base_url,
                        timeout=self._client.timeout,
                        max_retries=self._client.max_retries
                    )
                return self._client._sale_listings

            @property
            def sale_by_id(self) -> SaleListingByIdClient:
                """Access the sale listing by ID client."""
                if self._client._sale_listing is None:
                    self._client._sale_listing = SaleListingByIdClient(
                        api_key=self._client.api_key,
                        base_url=self._client.base_url,
                        timeout=self._client.timeout,
                        max_retries=self._client.max_retries
                    )
                return self._client._sale_listing

        if not hasattr(self, '_listings_client'):
            self._listings_client = ListingsClient(self)
        return self._listings_client

    async def close(self) -> None:
        """Close the HTTP client session and all sub-clients."""
        if self._client:
            await self._client.aclose()
            self._client = None
            
        # Clear cached clients
        self._property_data = None
        self._property_record = None
        self._random_properties = None
        self._market_data = None
        self._rental_listings = None
        self._rental_listing = None
        self._sale_listings = None
        self._sale_listing = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        model: type[BaseModel] | None = None,
    ) -> Any:
        """
        Make an HTTP request to the RentCast API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: Request body as JSON
            model: Pydantic model to parse response into

        Returns:
            Parsed response data or model instance

        Raises:
            RentCastError: For request/response handling errors
            RentCastValidationError: For response validation errors
            RentCastRateLimitError: When rate limited
            RentCastAuthenticationError: For authentication failures
            RentCastAPIError: For other API errors
        """
        if self._client is None:
            await self.start()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.client_params.get("headers", {}).copy()

        request_kwargs = {
            "method": method,
            "url": url,
            "params": params or {},
            "headers": headers,
        }

        if json_data is not None:
            request_kwargs["json"] = json_data

        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(**request_kwargs)
                response.raise_for_status()
                data = response.json()

                if model is not None:
                    return model.model_validate(data)
                return data

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                error_data = e.response.json() if e.response.content else {}

                if status_code == 401:
                    raise RentCastAuthenticationError(
                        "Invalid API key or authentication failed",
                        status_code=status_code,
                        response=error_data,
                    ) from e
                elif status_code == 429:
                    retry_after = int(e.response.headers.get("Retry-After", "60"))
                    if attempt < self.max_retries:
                        await asyncio.sleep(retry_after)
                        continue
                    raise RentCastRateLimitError(
                        "Rate limit exceeded",
                        status_code=status_code,
                        retry_after=retry_after,
                        response=error_data,
                    ) from e
                elif status_code >= 500:
                    if attempt < self.max_retries:
                        await asyncio.sleep(2**attempt)  # Exponential backoff
                        continue
                    raise RentCastAPIError(
                        "Server error",
                        status_code=status_code,
                        response=error_data,
                    ) from e
                else:
                    error_msg = error_data.get("message", str(e))
                    if status_code == 400:
                        raise RentCastValidationError(
                            error_msg,
                            status_code=status_code,
                            response=error_data,
                        ) from e
                    raise RentCastAPIError(
                        error_msg,
                        status_code=status_code,
                        response=error_data,
                    ) from e

            except (httpx.RequestError, ValidationError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                    continue
                if isinstance(e, ValidationError):
                    raise RentCastValidationError(
                        "Response validation failed",
                        errors=e.errors(),
                    ) from e
                raise RentCastError(f"Request failed: {str(e)}") from e

        raise RentCastError(
            f"Max retries ({self.max_retries}) exceeded. Last error: {str(last_exception)}"
        ) from last_exception

def get_rentcast_client():
    """Dependency to get RentCast client instance."""
    api_key = os.getenv("RENT_CAST_API_KEY")
    if not api_key:
        raise ValueError("RENT_CAST_API_KEY environment variable not set")
    return RentCastClient()

