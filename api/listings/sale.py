"""
RentCast Sale Listings API client implementation.

This module provides access to RentCast's sale listings endpoints.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

from app.core.third_party_integrations.rent_cast.api.listings._schema import (
    SaleListingsResponse,
)
from app.core.third_party_integrations.rent_cast.client import RentCastClient

# Re-export for backward compatibility
RentCastBaseModel = BaseModel

# Type aliases for better readability
OptionalStr = str | None
OptionalFloat = float | None
OptionalInt = int | None



class SaleListingsClient:
    """Client for interacting with RentCast's sale listings endpoints."""

    def __init__(self, client: RentCastClient):
        """Initialize the SaleListingsClient.

        Args:
            client: An instance of RentCastClient for making API requests.
        """
        self._client = client

    async def get_sale_listings(
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
            "Land",
        ]
        | None = None,
        bedrooms: OptionalFloat = None,
        bathrooms: OptionalFloat = None,
        status: Literal["Active", "Inactive"] = "Active",
        days_old: OptionalInt = None,
        limit: int = 50,
        offset: int = 0,
    ) -> SaleListingsResponse:
        """Search for sale listings based on various criteria.

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
            SaleListingsResponse: The response containing matching sale listings.

        Raises:
            RentCastError: If the API request fails or returns an error.
        """
        # Validate parameters
        if limit < 1 or limit > 500:
            raise ValueError("Limit must be between 1 and 500")
            
        if offset < 0:
            raise ValueError("Offset must be 0 or greater")
            
        if (latitude is not None or longitude is not None) and radius is None:
            raise ValueError("Radius is required when using latitude/longitude")
            
        if (latitude is None or longitude is None) and radius is not None:
            raise ValueError("Latitude and longitude are required when using radius")
        
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
        response = await self._client._request(
            method="GET",
            endpoint="/listings/sale",
            params=params,
        )
        
        # Parse and return the response
        return SaleListingsResponse(**response)
