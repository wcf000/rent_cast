"""
Pydantic models for RentCast property listings data.

This module defines the data models used for representing property listings
from the RentCast API responses.
"""

from datetime import datetime
from enum import Enum
from typing import Optional,Any

from pydantic import BaseModel, Field, field_validator

from .common import RentCastBaseModel


class PropertyType(str, Enum):
    """Enumeration of property types supported by RentCast API."""
    
    SINGLE_FAMILY = "Single Family"
    CONDO = "Condo"
    TOWNHOUSE = "Townhouse"
    MANUFACTURED = "Manufactured"
    MULTI_FAMILY = "Multi-Family"
    APARTMENT = "Apartment"
    LAND = "Land"


class ListingStatus(str, Enum):
    """Enumeration of possible listing statuses."""
    
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class ListingType(str, Enum):
    """Enumeration of listing types."""
    
    STANDARD = "Standard"
    # Add other listing types as needed


class HOADetails(RentCastBaseModel):
    """Model for Homeowners Association (HOA) details."""
    
    fee: Optional[float] = Field(
        None,
        description="Monthly HOA fee, if applicable.",
        ge=0,
        example=150.0
    )


class ContactInfo(RentCastBaseModel):
    """Base model for contact information."""
    
    name: Optional[str] = Field(
        None,
        description="The name of the contact person or entity.",
        example="John Doe"
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number.",
        example="555-123-4567"
    )
    email: Optional[str] = Field(
        None,
        description="Contact email address.",
        example="contact@example.com"
    )
    website: Optional[str] = Field(
        None,
        description="Website URL.",
        example="https://example.com"
    )


class ListingAgent(ContactInfo):
    """Model for listing agent information."""
    pass


class ListingOffice(ContactInfo):
    """Model for listing office information."""
    pass


class ListingHistoryEvent(RentCastBaseModel):
    """Model for a single historical event in a listing's history."""
    
    event: str = Field(
        ...,
        description="Type of event (e.g., 'Sale Listing').",
        example="Sale Listing"
    )
    price: float = Field(
        ...,
        description="Listing price at the time of the event.",
        ge=0,
        example=450000.0
    )
    listing_type: str = Field(
        ...,
        alias="listingType",
        description="Type of listing (e.g., 'Standard').",
        example="Standard"
    )
    listed_date: datetime = Field(
        ...,
        alias="listedDate",
        description="Date when the property was listed.",
        example="2024-01-01T00:00:00Z"
    )
    removed_date: Optional[datetime] = Field(
        None,
        alias="removedDate",
        description="Date when the listing was removed, if applicable.",
        example="2024-06-01T00:00:00Z"
    )
    days_on_market: int = Field(
        ...,
        alias="daysOnMarket",
        description="Number of days the property was on the market at the time of the event.",
        ge=0,
        example=30
    )


class ListingHistory(RentCastBaseModel):
    """Model for a listing's history, keyed by date."""
    
    __root__: dict[str, ListingHistoryEvent]
    
    def __getitem__(self, key: str) -> ListingHistoryEvent:
        return self.__root__[key]
    
    def get(self, key: str, default: Any = None) -> ListingHistoryEvent:
        return self.__root__.get(key, default)
    
    def items(self):
        return self.__root__.items()
    
    def keys(self):
        return self.__root__.keys()
    
    def values(self):
        return self.__root__.values()


class SaleListing(RentCastBaseModel):
    """Model representing a property listing for sale."""
    
    id: str = Field(
        ...,
        description="Unique identifier for the listing.",
        example="123-Main-St-Anytown-CA-12345"
    )
    formatted_address: str = Field(
        ...,
        alias="formattedAddress",
        description="Full formatted address of the property.",
        example="123 Main St, Anytown, CA 12345"
    )
    address_line1: str = Field(
        ...,
        alias="addressLine1",
        description="First line of the property address.",
        example="123 Main St"
    )
    address_line2: Optional[str] = Field(
        None,
        alias="addressLine2",
        description="Second line of the property address, if applicable.",
        example="Apt 4B"
    )
    city: str = Field(
        ...,
        description="City where the property is located.",
        example="Anytown"
    )
    state: str = Field(
        ...,
        description="2-letter state code where the property is located.",
        example="CA",
        min_length=2,
        max_length=2
    )
    zip_code: str = Field(
        ...,
        alias="zipCode",
        description="ZIP code of the property.",
        example="12345",
        min_length=5,
        max_length=10
    )
    county: str = Field(
        ...,
        description="County where the property is located.",
        example="Example County"
    )
    latitude: float = Field(
        ...,
        description="Latitude coordinate of the property.",
        example=37.7749,
        ge=-90,
        le=90
    )
    longitude: float = Field(
        ...,
        description="Longitude coordinate of the property.",
        example=-122.4194,
        ge=-180,
        le=180
    )
    property_type: str = Field(
        ...,
        alias="propertyType",
        description="Type of property.",
        example="Single Family"
    )
    bedrooms: float = Field(
        ...,
        description="Number of bedrooms in the property.",
        ge=0,
        example=3.0
    )
    bathrooms: float = Field(
        ...,
        description="Number of bathrooms in the property.",
        ge=0,
        example=2.5
    )
    square_footage: Optional[int] = Field(
        None,
        alias="squareFootage",
        description="Total living area in square feet.",
        ge=0,
        example=1800
    )
    lot_size: Optional[int] = Field(
        None,
        alias="lotSize",
        description="Size of the lot in square feet.",
        ge=0,
        example=5000
    )
    year_built: Optional[int] = Field(
        None,
        alias="yearBuilt",
        description="Year the property was built.",
        ge=1700,
        le=datetime.now().year + 1,
        example=2000
    )
    hoa: Optional[HOADetails] = Field(
        None,
        description="HOA (Homeowners Association) details, if applicable."
    )
    status: str = Field(
        ...,
        description="Current status of the listing.",
        example="Active"
    )
    price: float = Field(
        ...,
        description="Current listing price.",
        ge=0,
        example=450000.0
    )
    listing_type: str = Field(
        ...,
        alias="listingType",
        description="Type of listing.",
        example="Standard"
    )
    listed_date: datetime = Field(
        ...,
        alias="listedDate",
        description="Date when the property was listed.",
        example="2024-01-01T00:00:00Z"
    )
    removed_date: Optional[datetime] = Field(
        None,
        alias="removedDate",
        description="Date when the listing was removed, if applicable.",
        example="2024-06-01T00:00:00Z"
    )
    created_date: datetime = Field(
        ...,
        alias="createdDate",
        description="Date when the listing was created in the system.",
        example="2024-01-01T00:00:00Z"
    )
    last_seen_date: datetime = Field(
        ...,
        alias="lastSeenDate",
        description="Most recent date when the listing was seen/updated.",
        example="2024-05-26T12:00:00Z"
    )
    days_on_market: int = Field(
        ...,
        alias="daysOnMarket",
        description="Number of days the property has been on the market.",
        ge=0,
        example=30
    )
    mls_name: Optional[str] = Field(
        None,
        alias="mlsName",
        description="Name of the MLS (Multiple Listing Service) where the property is listed.",
        example="CRMLS"
    )
    mls_number: Optional[str] = Field(
        None,
        alias="mlsNumber",
        description="MLS number for the listing.",
        example="OC24012345"
    )
    listing_agent: Optional[ListingAgent] = Field(
        None,
        alias="listingAgent",
        description="Information about the listing agent."
    )
    listing_office: Optional[ListingOffice] = Field(
        None,
        alias="listingOffice",
        description="Information about the listing office."
    )
    history: Optional[ListingHistory] = Field(
        None,
        description="Historical data for the listing, keyed by date."
    )
    
    @field_validator('property_type')
    @classmethod
    def validate_property_type(cls, v: str) -> str:
        """Validate that the property type is one of the allowed values."""
        valid_types = [t.value for t in PropertyType]
        if v not in valid_types:
            raise ValueError(f"Property type must be one of {valid_types}")
        return v
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate that the status is one of the allowed values."""
        valid_statuses = [s.value for s in ListingStatus]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v

