"""
RentCast Rental Listings Models.

This module contains Pydantic models for handling rental listing data
from the RentCast API.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class PropertyType(str, Enum):
    """Enumeration of property types."""
    
    SINGLE_FAMILY = "Single Family"
    MULTI_FAMILY = "Multi Family"
    CONDO = "Condo"
    TOWNHOUSE = "Townhouse"
    APARTMENT = "Apartment"
    MANUFACTURED = "Manufactured"
    LAND = "Land"
    OTHER = "Other"


class ListingStatus(str, Enum):
    """Enumeration of listing statuses."""
    
    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"
    CANCELED = "Canceled"
    EXPIRED = "Expired"
    WITHDRAWN = "Withdrawn"
    TEMPORARILY_WITHDRAWN = "Temporarily Withdrawn"


class ListingType(str, Enum):
    """Enumeration of listing types."""
    
    STANDARD = "Standard"
    AUCTION = "Auction"
    FORECLOSURE = "Foreclosure"
    SHORT_SALE = "Short Sale"
    NEW_CONSTRUCTION = "New Construction"
    LEASE_OPTION = "Lease Option"
    LEASE_PURCHASE = "Lease Purchase"
    RENT_TO_OWN = "Rent to Own"


class HOADetails(BaseModel):
    """Model for HOA (Homeowners Association) details."""
    
    fee: float | None = Field(
        default=None,
        description="Monthly HOA fee in USD, if applicable.",
        examples=[45.0],
    )


class ContactInfo(BaseModel):
    """Model for contact information."""
    
    name: str | None = Field(
        default=None,
        description="Full name of the contact person.",
        examples=["John Doe"],
    )
    phone: str | None = Field(
        default=None,
        description="Phone number of the contact person.",
        examples=["555-123-4567"],
    )
    email: str | None = Field(
        default=None,
        description="Email address of the contact person.",
        examples=["john.doe@example.com"],
    )
    website: str | None = Field(
        default=None,
        description="Website URL of the contact person or company.",
        examples=["https://example.com"],
    )


class ListingAgent(ContactInfo):
    """Model for listing agent information."""
    
    license_number: str | None = Field(
        default=None,
        alias="licenseNumber",
        description="License number of the listing agent.",
        examples=["123456"],
    )


class ListingOffice(ContactInfo):
    """Model for listing office information."""
    
    license_number: str | None = Field(
        default=None,
        alias="licenseNumber",
        description="License number of the listing office.",
        examples=["ABC123"],
    )


class ListingHistoryEvent(BaseModel):
    """Model for a single event in the listing history."""
    
    event: str = Field(..., description="Type of event.")
    price: float | None = Field(
        default=None,
        description="Price at the time of the event.",
    )
    listing_type: str | None = Field(
        default=None,
        alias="listingType",
        description="Type of listing at the time of the event.",
    )
    listed_date: datetime | None = Field(
        default=None,
        alias="listedDate",
        description="Date when the property was listed.",
    )
    removed_date: datetime | None = Field(
        default=None,
        alias="removedDate",
        description="Date when the property was removed from the market.",
    )
    days_on_market: int | None = Field(
        default=None,
        alias="daysOnMarket",
        description="Number of days the property was on the market at the time of the event.",
    )


ListingHistory = dict[str, ListingHistoryEvent]


class RentalListing(BaseModel):
    """Model representing a rental property listing."""
    
    id: str = Field(..., description="Unique identifier for the listing.")
    formatted_address: str = Field(
        ...,
        alias="formattedAddress",
        description="Full formatted address of the property.",
    )
    address_line1: str | None = Field(
        default=None,
        alias="addressLine1",
        description="First line of the address.",
    )
    address_line2: str | None = Field(
        default=None,
        alias="addressLine2",
        description="Second line of the address.",
    )
    city: str = Field(..., description="City where the property is located.")
    state: str = Field(..., description="State where the property is located.")
    zip_code: str = Field(
        ...,
        alias="zipCode",
        description="ZIP code where the property is located.",
    )
    county: str | None = Field(
        default=None,
        description="County where the property is located.",
    )
    latitude: float = Field(..., description="Latitude coordinate of the property.")
    longitude: float = Field(..., description="Longitude coordinate of the property.")
    property_type: PropertyType = Field(
        ...,
        alias="propertyType",
        description="Type of the property.",
    )
    bedrooms: float | None = Field(
        default=None,
        description="Number of bedrooms in the property.",
    )
    bathrooms: float | None = Field(
        default=None,
        description="Number of bathrooms in the property.",
    )
    square_footage: int | None = Field(
        default=None,
        alias="squareFootage",
        description="Total living area in square feet.",
    )
    lot_size: int | None = Field(
        default=None,
        alias="lotSize",
        description="Total lot size in square feet.",
    )
    year_built: int | None = Field(
        default=None,
        alias="yearBuilt",
        description="Year the property was built.",
    )
    hoa: HOADetails | None = Field(
        default=None,
        description="HOA (Homeowners Association) details, if applicable.",
    )
    status: ListingStatus = Field(..., description="Current status of the listing.")
    price: float = Field(..., description="Current listing price in USD.")
    listing_type: ListingType = Field(
        ...,
        alias="listingType",
        description="Type of the listing.",
    )
    listed_date: datetime | None = Field(
        default=None,
        alias="listedDate",
        description="Date when the property was listed.",
    )
    removed_date: datetime | None = Field(
        default=None,
        alias="removedDate",
        description="Date when the property was removed from the market.",
    )
    created_date: datetime | None = Field(
        default=None,
        alias="createdDate",
        description="Date when the listing was created in the system.",
    )
    last_seen_date: datetime | None = Field(
        default=None,
        alias="lastSeenDate",
        description="Date when the listing was last seen/updated.",
    )
    days_on_market: int | None = Field(
        default=None,
        alias="daysOnMarket",
        description="Number of days the property has been on the market.",
    )
    mls_name: str | None = Field(
        default=None,
        alias="mlsName",
        description="Name of the MLS where the listing is published.",
    )
    mls_number: str | None = Field(
        default=None,
        alias="mlsNumber",
        description="MLS number of the listing.",
    )
    listing_agent: ListingAgent | None = Field(
        default=None,
        alias="listingAgent",
        description="Information about the listing agent.",
    )
    listing_office: ListingOffice | None = Field(
        default=None,
        alias="listingOffice",
        description="Information about the listing office.",
    )
    history: ListingHistory | None = Field(
        default=None,
        description="History of the listing, keyed by date.",
    )

    @field_validator("property_type", mode="before")
    @classmethod
    def validate_property_type(cls, v: Any) -> str:
        """Convert property type string to title case if it's a string."""
        if isinstance(v, str):
            return v.title()
        return v

    @field_validator("status", "listing_type", mode="before")
    @classmethod
    def validate_enum_fields(cls, v: Any, info: ValidationInfo) -> str:
        """Convert enum-like string fields to title case if they're strings."""
        if isinstance(v, str):
            return v.title()
        return v


class RentalListingsResponse(BaseModel):
    """Response model for rental listings search results."""
    
    data: list[RentalListing] = Field(
        default_factory=list,
        description="List of rental listings matching the search criteria.",
    )
    total: int = Field(
        ...,
        description="Total number of listings matching the search criteria.",
    )
    page: int = Field(
        ...,
        description="Current page number of the results.",
    )
    limit: int = Field(
        ...,
        description="Maximum number of results per page.",
    )

    class Config:
        """Pydantic model configuration."""
        
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": "2005-Arborside-Dr,-Austin,-TX-78754",
                        "formattedAddress": "2005 Arborside Dr, Austin, TX 78754",
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
                "limit": 10
            }
        }
