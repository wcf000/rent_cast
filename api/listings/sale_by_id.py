"""
RentCast Sale Listing by ID API client implementation.

This module provides access to RentCast's sale listing by ID endpoint.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.core.third_party_integrations.rent_cast.client import RentCastClient
from app.core.third_party_integrations.rent_cast.models.property_listings import (
    SaleListing,
)

# Re-export for backward compatibility
RentCastBaseModel = BaseModel

# Type alias for better readability
OptionalStr = str | None


class SaleListingByIdResponse(RentCastBaseModel):
    """Response model for a single sale listing by ID."""

    data: SaleListing = Field(
        ...,
        description="The sale listing matching the specified ID.",
    )


class SaleListingByIdClient:
    """Client for interacting with RentCast's sale listing by ID endpoint."""

    def __init__(self, client: RentCastClient):
        """Initialize the SaleListingByIdClient.

        Args:
            client: An instance of RentCastClient for making API requests.
        """
        self._client = client

    async def get_sale_listing_by_id(
        self,
        listing_id: str,
    ) -> SaleListingByIdResponse:
        """Get a single sale listing by its ID.

        Args:
            listing_id: The ID of the property listing to retrieve.
                This should be in the same format as returned by other RentCast API endpoints.

        Returns:
            SaleListingByIdResponse: The response containing the sale listing.

        Raises:
            RentCastError: If the API request fails or returns an error.
            ValueError: If the listing_id is empty or None.
        """
        if not listing_id:
            raise ValueError("Listing ID cannot be empty or None")

        # Prepare the endpoint URL with the listing ID
        endpoint = f"listings/sale/{listing_id}"

        # Make the API request
        response = await self._client.get(endpoint)

        # Parse and return the response
        return SaleListingByIdResponse(data=SaleListing(**response))
