"""
RentCast Rental Listings API client implementation.

This module provides access to RentCast's rental listings endpoints.
"""
from __future__ import annotations

from typing import Any, Literal

from app.core.third_party_integrations.rent_cast.api.listings._schema import (
    RentalListingsResponse,
)
from app.core.third_party_integrations.rent_cast.client import RentCastClient

# Type aliases for better readability
OptionalStr = str | None
OptionalFloat = float | None
OptionalInt = int | None


class RentalListingsClient:
    """Client for interacting with RentCast's rental listings endpoints."""

    def __init__(self, client: RentCastClient):
        """Initialize the RentalListingsClient.

        Args:
            client: An instance of RentCastClient for making API requests.
        """
        self._client = client

    async def get_rental_listings(
        self,
        address: OptionalStr = None,
        city: str = "Austin",
        state: str = "TX",
        zip_code: OptionalStr = None,
        latitude: OptionalFloat = None,
        longitude: OptionalFloat = None,
        radius: OptionalFloat = None,
        property_type: Literal[
            "Single Family",
            "Condo",
            "Townhouse",
            "Manufactured",
            "Multi-Family",
            "Apartment",
        ]
        | None = None,
        bedrooms: OptionalFloat = None,
        bathrooms: OptionalFloat = None,
        status: Literal["Active", "Inactive"] = "Active",
        days_old: OptionalInt = None,
        limit: int = 50,
        offset: int = 0,
    ) -> RentalListingsResponse:
        """Search for rental listings based on various criteria.

        Args:
            address: The full address of the property, in the format of 'Street, City, State, Zip'.
            city: The name of the city to search in (case-sensitive).
            state: The 2-character state abbreviation to search in (case-sensitive).
            zip_code: The 5-digit zip code to search in.
            latitude: The latitude of the search area (use with longitude and radius).
            longitude: The longitude of the search area (use with latitude and radius).
            radius: The radius in miles for the search area (max 100 miles).
            property_type: The type of property to filter by.
            bedrooms: The number of bedrooms to filter by (use 0 for studio).
            bathrooms: The number of bathrooms to filter by (supports fractions).
            status: The listing status to filter by ('Active' or 'Inactive').
            days_old: The maximum number of days since the property was listed.
            limit: The maximum number of listings to return (1-500, default 50).
            offset: The index of the first listing to return (for pagination).

        Returns:
            RentalListingsResponse: The response containing matching rental listings.

        Raises:
            RentCastError: If the API request fails or returns an error.
            ValueError: If invalid parameters are provided.
        """
        # Validate parameters
        if limit < 1 or limit > 500:
            raise ValueError("Limit must be between 1 and 500")
        if radius is not None and (radius <= 0 or radius > 100):
            raise ValueError("Radius must be between 0.1 and 100 miles")
        if days_old is not None and days_old < 1:
            raise ValueError("Days old must be at least 1")

        # Prepare query parameters
        params: dict[str, Any] = {
            "city": city,
            "state": state,
            "status": status,
            "limit": limit,
            "offset": offset,
        }

        # Add optional parameters if provided
        if address:
            params["address"] = address
        if zip_code:
            params["zipCode"] = zip_code
        if latitude is not None:
            params["latitude"] = latitude
        if longitude is not None:
            params["longitude"] = longitude
        if radius is not None:
            params["radius"] = radius
        if property_type:
            params["propertyType"] = property_type
        if bedrooms is not None:
            params["bedrooms"] = bedrooms
        if bathrooms is not None:
            params["bathrooms"] = bathrooms
        if days_old is not None:
            params["daysOld"] = days_old

        # Make the API request
        response = await self._client.get("listings/rental/long-term", params=params)

        # Parse and return the response
        return RentalListingsResponse(**response)
