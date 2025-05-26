"""
RentCast Property Record by ID API client.

This module provides a client for fetching property records by ID from the RentCast API.
"""
from __future__ import annotations

import logging

from pydantic import ValidationError

from ...api._exceptions import RentCastError, RentCastValidationError
from ...client import RentCastClient
from ...models import Property

logger = logging.getLogger(__name__)


class PropertyRecordClient(RentCastClient):
    """Client for fetching property records by ID from the RentCast API."""

    async def get_property_by_id(
        self,
        property_id: str,
    ) -> Property:
        """
        Fetch a property record by its ID.

        Args:
            property_id: The unique identifier for the property.
                        This is typically in the format "Street-Address,-City,-State-Zip"
                        (e.g., "5500-Grand-Lake-Dr,-San-Antonio,-TX-78244")

        Returns:
            Property: A Property model instance containing the property details.

        Raises:
            RentCastValidationError: If the property_id is empty or invalid.
            RentCastError: For other API errors or if the property is not found.

        Example:
            ```python
            client = PropertyRecordClient()
            property = await client.get_property_by_id("5500-Grand-Lake-Dr,-San-Antonio,-TX-78244")
            print(property.address)  # "5500 Grand Lake Dr, San Antonio, TX 78244"
            ```
        """
        if not property_id or not isinstance(property_id, str) or not property_id.strip():
            raise RentCastValidationError("Property ID cannot be empty")

        try:
            # The API returns a single property object for this endpoint
            data = await self._request(
                "GET",
                f"/properties/{property_id}",
            )

            # Validate and parse the response into a Property model
            return Property.model_validate(data)

        except ValidationError as e:
            logger.error("Failed to validate property data: %s", str(e))
            raise RentCastValidationError("Invalid property data received from API") from e
        except Exception as e:
            logger.error("Failed to fetch property by ID: %s", str(e))
            raise RentCastError(f"Failed to fetch property: {str(e)}") from e

