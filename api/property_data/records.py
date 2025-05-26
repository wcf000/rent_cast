"""
RentCast Properties API client.

This module provides a client for interacting with the RentCast Properties API endpoints.
"""
from __future__ import annotations

import logging
from typing import Any, overload

from pydantic import ValidationError

from ...api._exceptions import RentCastValidationError
from ...client import RentCastClient
from ...models import (
    Property,
    PropertySearchParams,
    PropertySearchResponse,
    PropertyType,
)

logger = logging.getLogger(__name__)


class PropertiesClient(RentCastClient):
    """
    Client for interacting with the RentCast Properties API.
    """

    @overload
    async def search_properties(
        self,
        *,
        search_params: PropertySearchParams,
        **kwargs,
    ) -> PropertySearchResponse:
        ...

    @overload
    async def search_properties(
        self,
        *,
        address: str | None = None,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        radius: float | None = None,
        property_type: PropertyType | None = None,
        bedrooms: float | None = None,
        bathrooms: float | None = None,
        sale_date_range: int | None = None,
        limit: int = 50,
        offset: int = 0,
        **kwargs,
    ) -> PropertySearchResponse:
        ...

    async def search_properties(
        self,
        search_params: PropertySearchParams | None = None,
        **kwargs,
    ) -> PropertySearchResponse:
        """
        Search for property records in the RentCast database.
        """
        if search_params is None:
            try:
                search_params = PropertySearchParams(**kwargs)
            except ValidationError as e:
                raise RentCastValidationError(
                    "Invalid search parameters",
                    errors=e.errors(),
                ) from e

        params = search_params.to_query_params()
        data = await self._request("GET", "/properties", params=params)
        return PropertySearchResponse.model_validate(data)

    async def get_property(
        self,
        property_id: str,
        **kwargs,
    ) -> Property:
        """
        Get detailed information about a specific property by its ID.
        """
        data = await self._request("GET", f"/properties/{property_id}", **kwargs)
        return Property.model_validate(data)

    async def search_by_address(
        self,
        address: str,
        radius: float | None = None,
        **kwargs: Any,
    ) -> PropertySearchResponse:
        """
        Search for properties by address.
        """
        params = {"address": address}
        if radius is not None:
            params["radius"] = radius
        params.update(kwargs)

        return await self.search_properties(**params)

    async def search_by_coordinates(
        self,
        latitude: float,
        longitude: float,
        radius: float,
        **kwargs: Any,
    ) -> PropertySearchResponse:
        """
        Search for properties within a radius of geographic coordinates.
        """
        return await self.search_properties(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            **kwargs
        )
