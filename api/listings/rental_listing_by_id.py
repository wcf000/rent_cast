"""
RentCast Rental Listing by ID API client implementation.

This module provides access to fetch a single rental listing by its ID
from the RentCast API.
"""
from __future__ import annotations

from app.core.third_party_integrations.rent_cast.client import RentCastClient
from app.core.third_party_integrations.rent_cast.models.rental_listings import (
    RentalListing,
)

# Re-export for backward compatibility


class RentalListingByIdClient:
    """Client for fetching a single rental listing by ID from RentCast API."""

    def __init__(self, client: RentCastClient):
        """Initialize the RentalListingByIdClient.

        Args:
            client: An instance of RentCastClient for making API requests.
        """
        self._client = client

    async def get_rental_listing_by_id(self, listing_id: str) -> RentalListing | None:
        """Fetch a single rental listing by its ID.

        Args:
            listing_id: The unique identifier of the rental listing to fetch.
                This should be in the format "Street-Address,-City,-ST-ZIP".

        Returns:
            A RentalListing object if found, None otherwise.

        Raises:
            ValueError: If the listing_id is empty or None.
            RentCastError: If the API request fails.
        """
        if not listing_id:
            raise ValueError("Listing ID cannot be empty or None")

        # Make the API request
        response = await self._client.get(f"listings/rental/long-term/{listing_id}")

        # If the response is empty, return None
        if not response:
            return None

        # Parse and return the response as a RentalListing
        return RentalListing(**response)
