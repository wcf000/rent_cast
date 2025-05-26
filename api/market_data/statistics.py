"""
RentCast Market Data API Client.

This module provides a client for interacting with the RentCast Market Data API.
"""
from __future__ import annotations

import logging
from datetime import date

from pydantic import ValidationError

from ...api._exceptions import RentCastError
from ...client import RentCastClient
from ...models.market_data import (
    MarketDataInterval,
    MarketDataMetric,
    MarketDataResponse,
)
from ._exceptions import InvalidRequestError, MarketDataError
from ._schema import MarketDataRequest

logger = logging.getLogger(__name__)

class MarketDataClient:
    """Client for interacting with the RentCast Market Data API."""
    
    def __init__(self, client: RentCastClient):
        """Initialize the MarketDataClient.
        
        Args:
            client: An instance of RentCastClient for making API requests.
        """
        self._client = client
        self._base_path = "market-data"
    
    async def get_market_data(
        self,
        *,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
        property_types: list[str] = None,
        metrics: list[MarketDataMetric] = None,
        interval: MarketDataInterval = MarketDataInterval.MONTHLY,
        start_date: date,
        end_date: date
    ) -> MarketDataResponse:
        """Get market data for a specific location and time period.
        
        Args:
            city: City name (required if zip_code not provided)
            state: Two-letter state code (required if zip_code not provided)
            zip_code: ZIP code (required if city/state not provided)
            property_types: List of property types to include
            metrics: List of metrics to retrieve
            interval: Time interval for the data points
            start_date: Start date for the data range
            end_date: End date for the data range
            
        Returns:
            MarketDataResponse containing the requested market data
            
        Raises:
            InvalidRequestError: If the request parameters are invalid
            MarketDataError: If there's an error fetching the market data
        """
        try:
            # Build and validate the request
            request = MarketDataRequest(
                city=city,
                state=state,
                zip_code=zip_code,
                property_types=property_types or [],
                metrics=metrics or list(MarketDataMetric),
                interval=interval,
                start_date=start_date,
                end_date=end_date
            )
            
            # Make the API request
            response = await self._client.get(
                self._base_path,
                params=request.dict(by_alias=True, exclude_none=True)
            )
            
            # Parse and return the response
            return MarketDataResponse(**response)
            
        except ValidationError as e:
            logger.error(f"Validation error in market data request: {e}")
            raise InvalidRequestError(f"Invalid market data request: {e}") from e
        except RentCastError as e:
            logger.error(f"Error fetching market data: {e}")
            raise MarketDataError(f"Failed to fetch market data: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in market data client: {e}")
            raise MarketDataError(f"Unexpected error: {e}") from e