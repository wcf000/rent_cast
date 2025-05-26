"""
RentCast Random Properties API client.

This module provides a client for interacting with the RentCast Random Properties API endpoint.
"""
from __future__ import annotations

import logging
from typing import overload

from pydantic import Field, ValidationError

from ...api._exceptions import RentCastValidationError
from ...client import RentCastClient
from ...models import Property, PropertySearchResponse

logger = logging.getLogger(__name__)


class RandomPropertyParams:
    """Parameters for the random properties endpoint."""
    limit: int = Field(
        default=5,
        ge=1,
        le=500,
        description="Number of random properties to return (1-500)",
    )

    def to_query_params(self) -> dict[str, str]:
        """Convert the model to query parameters for API requests."""
        return {"limit": str(self.limit)}


class RandomPropertyClient(RentCastClient):
    """Client for interacting with the RentCast Random Properties API."""

    @overload
    async def get_random_properties(
        self,
        *,
        params: RandomPropertyParams,
    ) -> PropertySearchResponse:
        ...

    @overload
    async def get_random_properties(
        self,
        *,
        limit: int = 5,
    ) -> PropertySearchResponse:
        ...

    async def get_random_properties(
        self,
        params: RandomPropertyParams | None = None,
        **kwargs,
    ) -> PropertySearchResponse:
        """Get a list of randomly selected property records.

        Args:
            params: RandomPropertyParams instance with search parameters
            limit: Number of random properties to return (1-500)

        Returns:
            PropertySearchResponse containing the list of random properties

        Raises:
            RentCastValidationError: If input validation fails
            RentCastError: For other API errors
        """
        if params is None:
            try:
                params = RandomPropertyParams(**kwargs)
            except ValidationError as e:
                raise RentCastValidationError(
                    "Invalid parameters for random properties",
                    errors=e.errors(),
                ) from e

        query_params = params.to_query_params()
        data = await self._request("GET", "/properties/random", params=query_params)

        # The API returns a list of properties, but we need to wrap it in a PropertySearchResponse
        if isinstance(data, list):
            return PropertySearchResponse(
                properties=[Property.model_validate(prop) for prop in data],
                total=len(data),
                limit=len(data),
                offset=0,
                has_more=False,
            )

        # If the response format changes, try to parse it as a PropertySearchResponse
        return PropertySearchResponse.model_validate(data)