"""
Property data models for the RentCast API.
"""
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator

from .common import (
    MailingAddress,
    OwnerType,
    PropertyHistoryEvent,
    PropertyTaxYear,
    PropertyType,
)


class PropertyTax(BaseModel):
    """Tax information for a property."""
    amount: float | None = Field(None, description="Annual property tax amount in USD")
    year: int | None = Field(None, description="Assessment year")
    tax_rate: float | None = Field(
        None,
        alias="taxRate",
        description="Tax rate as a percentage (e.g., 1.5 for 1.5%)"
    )
    tax_year: int | None = Field(
        None,
        alias="taxYear",
        description="Year the tax rate is applicable for"
    )
    tax_assessment: dict[str, PropertyTaxYear] | None = Field(
        None,
        alias="taxAssessment",
        description="Tax assessment history by year"
    )


class PropertyOwner(BaseModel):
    """Information about the property owner."""
    names: list[str] = Field(
        default_factory=list,
        description="list of owner names"
    )
    type: OwnerType = Field(
        default=OwnerType.INDIVIDUAL,
        description="Type of owner (individual, business, etc.)"
    )
    mailing_address: MailingAddress | None = Field(
        None,
        alias="mailingAddress",
        description="Mailing address of the owner"
    )


class PropertyHistory(BaseModel):
    """Historical events for a property."""
    events: dict[str, PropertyHistoryEvent] = Field(
        default_factory=dict,
        description="dictionary of historical events by date"
    )
    last_sale: PropertyHistoryEvent | None = Field(
        None,
        alias="lastSale",
        description="Most recent sale event"
    )


class Property(BaseModel):
    """Main property data model."""
    # Core identifiers
    id: str = Field(..., description="Unique identifier for the property")
    property_id: str = Field(
        ...,
        alias="propertyId",
        description="Internal property ID"
    )
    listing_id: str | None = Field(
        None,
        alias="listingId",
        description="listing ID if available"
    )

    # Location information
    address: str = Field(..., description="Full property address")
    address_line1: str = Field(
        ...,
        alias="addressLine1",
        description="First line of the address"
    )
    address_line2: str | None = Field(
        None,
        alias="addressLine2",
        description="Second line of the address"
    )
    city: str = Field(..., description="City name")
    state: str = Field(..., description="2-letter state code")
    zip_code: str = Field(
        ...,
        alias="zipCode",
        description="ZIP code"
    )
    county: str | None = Field(None, description="County name")
    latitude: float | None = Field(None, description="Geographic latitude")
    longitude: float | None = Field(None, description="Geographic longitude")
    formatted_address: str = Field(
        ...,
        alias="formattedAddress",
        description="Formatted full address"
    )

    # Property characteristics
    property_type: PropertyType = Field(
        ...,
        alias="propertyType",
        description="Type of property"
    )
    bedrooms: float | None = Field(None, description="Number of bedrooms")
    bathrooms: float | None = Field(None, description="Number of bathrooms")
    square_feet: int | None = Field(
        None,
        alias="squareFeet",
        description="Total square footage"
    )
    lot_size: float | None = Field(
        None,
        alias="lotSize",
        description="Lot size in square feet"
    )
    year_built: int | None = Field(
        None,
        alias="yearBuilt",
        description="Year the property was built"
    )

    # Status and dates
    status: str | None = Field(None, description="Current status of the property")
    last_sold_date: datetime | None = Field(
        None,
        alias="lastSoldDate",
        description="Date of last sale"
    )
    last_sold_price: float | None = Field(
        None,
        alias="lastSoldPrice",
        description="Price of last sale in USD"
    )

    # Financial information
    price: float | None = Field(None, description="Current price in USD")
    price_per_square_foot: float | None = Field(
        None,
        alias="pricePerSquareFoot",
        description="Price per square foot in USD"
    )
    tax: PropertyTax | None = Field(None, description="Tax information")

    # Additional data
    owner_occupied: bool = Field(
        False,
        alias="ownerOccupied",
        description="Whether the property is owner-occupied"
    )
    owner: PropertyOwner | None = Field(None, description="Owner information")
    history: PropertyHistory | None = Field(
        None,
        description="Historical events and sales data"
    )

    # Links and external data
    image_url: HttpUrl | None = Field(
        None,
        alias="imageUrl",
        description="URL of property image if available"
    )
    details_url: HttpUrl | None = Field(
        None,
        alias="detailsUrl",
        description="URL for more details"
    )

    @field_validator('property_type', mode='before')
    @classmethod
    def validate_property_type(cls, v):
        if v and isinstance(v, str):
            try:
                return PropertyType(v.upper())
            except ValueError:
                return PropertyType.OTHER
        return v or PropertyType.OTHER


class PropertySearchResponse(BaseModel):
    """Response model for property search results."""
    properties: list[Property] = Field(
        default_factory=list,
        description="list of matching properties"
    )
    total: int = Field(0, description="Total number of results")
    limit: int = Field(50, description="Number of results per page")
    offset: int = Field(0, description="Pagination offset")
    has_more: bool = Field(
        False,
        alias="hasMore",
        description="Whether there are more results available"
    )

    @property
    def next_offset(self) -> int | None:
        """Calculate the offset for the next page of results."""
        if self.has_more:
            return self.offset + self.limit
        return None
