"""
Property valuation client for the RentCast API.

This module provides functionality to retrieve property value estimates and comparable
listings from the RentCast API.
"""
from __future__ import annotations

from typing import Any

from httpx import AsyncClient

from ...api._exceptions import RentCastValidationError
from ...client import RentCastClient
from ...models.property_valuation import (
    ComparableProperty,
    ValueEstimateParams,
    ValueEstimateResponse,
)


class PropertyValuationClient(RentCastClient):
    """Client for interacting with the RentCast Property Valuation API."""

    BASE_ENDPOINT = "property-value"

    def __init__(self, client: AsyncClient, api_key: str) -> None:
        """Initialize the PropertyValuationClient.

        Args:
            client: The async HTTP client to use for requests
            api_key: The RentCast API key
        """
        super().__init__(client, api_key)

    async def get_value_estimate(
        self,
        params: ValueEstimateParams,
    ) -> ValueEstimateResponse:
        """
        Get a property value estimate with comparable listings.

        Args:
            params: Parameters for the value estimate request

        Returns:
            ValueEstimateResponse containing the estimated value and comparables

        Raises:
            RentCastValidationError: If the request parameters are invalid
            RentCastAPIError: If the API request fails
        """
        # Validate that either address or lat/long is provided
        if not params.address and not (params.latitude and params.longitude):
            raise RentCastValidationError(
                "Either 'address' or both 'latitude' and 'longitude' must be provided"
            )

        # Convert params to query parameters
        query_params = params.to_query_params()
        
        # Make the API request
        response = await self._make_request(
            "GET",
            self.BASE_ENDPOINT,
            params=query_params,
        )

        # Process and validate the response
        return self._process_value_estimate_response(response)

    def _process_value_estimate_response(
        self, response_data: dict[str, Any]
    ) -> ValueEstimateResponse:
        """Process and validate the value estimate API response.

        Args:
            response_data: Raw response data from the API

        Returns:
            Validated ValueEstimateResponse object

        Raises:
            RentCastValidationError: If the response data is invalid
        """
        try:
            # Process comparables if present
            if "comparables" in response_data:
                comparables = [
                    ComparableProperty.model_validate(prop)
                    for prop in response_data["comparables"]
                ]
                response_data["comparables"] = comparables

            return ValueEstimateResponse.model_validate(response_data)

        except (KeyError, ValueError, TypeError) as e:
            raise RentCastValidationError(
                "Invalid response format from RentCast API"
            ) from e

    @classmethod
    def create(
        cls, client: AsyncClient, api_key: str
    ) -> "PropertyValuationClient":
        """Create a new instance of PropertyValuationClient.

        This is the preferred way to create a client instance as it ensures
        proper initialization and type checking.

        Args:
            client: The async HTTP client to use for requests
            api_key: The RentCast API key

        Returns:
            A new instance of PropertyValuationClient
        """
        return cls(client, api_key)
