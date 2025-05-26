"""
API response schemas for RentCast API clients.

This module contains Pydantic models for API responses that are shared across
multiple endpoints or need special handling.
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.third_party_integrations.rent_cast.models.common import RentCastBaseModel
from app.core.third_party_integrations.rent_cast.models.property_listings import (
    SaleListing,
)
from app.core.third_party_integrations.rent_cast.models.rental_listings import (
    RentalListing,
)

# Type variable for paginated response items
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """A generic paginated response model.
    
    This is a base class that can be used for any paginated API response.
    Subclasses should specify the concrete type parameter for the items.
    """
    data: list[T] = Field(
        ...,
        description="List of items in the current page."
    )
    total: int = Field(
        ...,
        description="Total number of items across all pages.",
        ge=0,
        example=1
    )
    page: int = Field(
        ...,
        description="Current page number (1-based).",
        ge=1,
        example=1
    )
    limit: int = Field(
        ...,
        description="Maximum number of items per page.",
        ge=1,
        le=500,
        example=50
    )


class RentalListingsResponse(PaginatedResponse[RentalListing]):
    """Response model for rental listings search.
    
    This extends the generic PaginatedResponse with rental listing specific
    documentation and defaults.
    """
    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": "2005-Arborside-Dr,-Austin,-TX-78754",
                        "formattedAddress": "2005 Arborside Dr, Austin, TX 78754",
                        "addressLine1": "2005 Arborside Dr",
                        "addressLine2": None,
                        "city": "Austin",
                        "state": "TX",
                        "zipCode": "78754",
                        "propertyType": "Single Family",
                        "bedrooms": 3,
                        "bathrooms": 2.5,
                        "price": 2200,
                        "status": "Active"
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 50
            }
        }


class SaleListingsResponse(RentCastBaseModel):
    """Response model for a collection of sale listings."""
    
    data: list[SaleListing] = Field(
        ...,
        description="list of sale listings matching the search criteria."
    )
    total: int = Field(
        ...,
        description="Total number of listings matching the search criteria.",
        ge=0,
        example=1
    )
    page: int = Field(
        ...,
        description="Current page number in the paginated results.",
        ge=1,
        example=1
    )
    limit: int = Field(
        ...,
        description="Maximum number of listings returned per page.",
        ge=1,
        le=500,
        example=50
    )
