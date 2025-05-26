"""
Property valuation models for the RentCast API.

This module contains models for property valuation and rent estimate data,
including value estimates, rent estimates, and comparable property listings.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator

from .common import PropertyType

# Generic type for response data (rent or price)
T = TypeVar('T', int, float)


class ListingType(str, Enum):
    """Enumeration of property listing types."""
    STANDARD = "Standard"
    PRE_FORECLOSURE = "Pre-foreclosure"
    FORECLOSURE = "Foreclosure"
    SHORT_SALE = "Short Sale"
    AUCTION = "Auction"
    BANK_OWNED = "Bank Owned"
    CORPORATE_OWNED = "Corporate Owned"
    HUD_OWNED = "HUD Owned"
    LEASE_OPTION = "Lease Option"
    NEW_CONSTRUCTION = "New Construction"
    NEW_LISTING = "New Listing"
    PRICE_REDUCED = "Price Reduced"
    COMING_SOON = "Coming Soon"
    PENDING = "Pending"
    CONTINGENT = "Contingent"
    BACK_ON_MARKET = "Back on Market"
    SOLD = "Sold"


class ComparableProperty(BaseModel):
    """Model for comparable property listings used in valuation."""
    id: str = Field(..., description="Unique identifier for the property")
    formatted_address: str = Field(
        ...,
        alias="formattedAddress",
        description="Full formatted address of the property"
    )
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
    zip_code: str = Field(..., alias="zipCode", description="ZIP code")
    county: str = Field(..., description="County name")
    latitude: float = Field(..., description="Geographic latitude")
    longitude: float = Field(..., description="Geographic longitude")
    property_type: str = Field(
        ...,
        alias="propertyType",
        description="Type of property"
    )
    bedrooms: float = Field(..., description="Number of bedrooms")
    bathrooms: float = Field(..., description="Number of bathrooms")
    square_footage: int = Field(
        ...,
        alias="squareFootage",
        description="Total living area in square feet"
    )
    lot_size: int | None = Field(
        None,
        alias="lotSize",
        description="Lot size in square feet"
    )
    year_built: int | None = Field(
        None,
        alias="yearBuilt",
        description="Year the property was built"
    )
    price: int = Field(..., description="Listing or sale price in USD")
    listing_type: str = Field(
        ...,
        alias="listingType",
        description="Type of listing"
    )
    listed_date: datetime | None = Field(
        None,
        alias="listedDate",
        description="Date when the property was listed"
    )
    removed_date: datetime | None = Field(
        None,
        alias="removedDate",
        description="Date when the listing was removed"
    )
    last_seen_date: datetime | None = Field(
        None,
        alias="lastSeenDate",
        description="Last time the listing was seen"
    )
    days_on_market: int = Field(
        ...,
        alias="daysOnMarket",
        description="Number of days the property was on the market"
    )
    distance: float = Field(
        ...,
        description="Distance from the subject property in miles"
    )
    days_old: int = Field(
        ...,
        alias="daysOld",
        description="Number of days since the listing was last seen"
    )
    correlation: float = Field(
        ...,
        description="Correlation score indicating similarity to the subject property"
    )

    @field_validator('property_type', mode='before')
    @classmethod
    def validate_property_type(cls, v):
        if v and isinstance(v, str):
            try:
                return PropertyType(v.upper().replace(" ", "_"))
            except ValueError:
                return v
        return v

    @field_validator('listing_type', mode='before')
    @classmethod
    def validate_listing_type(cls, v):
        if v and isinstance(v, str):
            try:
                return ListingType(v.replace(" ", "_").upper())
            except ValueError:
                return v
        return v


class BaseEstimateResponse(BaseModel, Generic[T]):
    """Base response model for property estimates (value or rent)."""
    value: T = Field(..., description="Estimated value in USD")
    range_low: T = Field(
        ...,
        alias="rangeLow",
        description="Lower bound of the estimated range in USD"
    )
    range_high: T = Field(
        ...,
        alias="rangeHigh",
        description="Upper bound of the estimated range in USD"
    )
    latitude: float = Field(
        ...,
        description="Latitude of the subject property"
    )
    longitude: float = Field(
        ...,
        description="Longitude of the subject property"
    )
    comparables: list[ComparableProperty] = Field(
        default_factory=list,
        description="List of comparable properties used in the estimation"
    )

    @property
    def value_range(self) -> tuple[T, T]:
        """Get the value range as a tuple (low, high)."""
        return (self.range_low, self.range_high)

    @property
    def range_midpoint(self) -> float:
        """Calculate the midpoint of the value range."""
        return (self.range_low + self.range_high) / 2

    @property
    def range_spread(self) -> float:
        """Calculate the spread of the value range."""
        return self.range_high - self.range_low

    def get_comparables_sorted(
        self,
        by: str = "correlation",
        descending: bool = True
    ) -> list[ComparableProperty]:
        """
        Get comparable properties sorted by a field.

        Args:
            by: Field to sort by (default: "correlation")
            descending: Whether to sort in descending order (default: True)

        Returns:
            List of comparable properties sorted by the specified field
        """
        if not self.comparables:
            return []

        if not hasattr(self.comparables[0], by):
            raise ValueError(f"Invalid sort field: {by}")

        return sorted(
            self.comparables,
            key=lambda x: getattr(x, by),
            reverse=descending
        )


class ValueEstimateResponse(BaseEstimateResponse[int]):
    """Response model for property value estimate."""
    value: int = Field(..., alias="price", description="Estimated property value in USD")
    range_low: int = Field(..., alias="priceRangeLow")
    range_high: int = Field(..., alias="priceRangeHigh")


class RentEstimateResponse(BaseEstimateResponse[int]):
    """Response model for property rent estimate."""
    value: int = Field(..., alias="rent", description="Estimated monthly rent in USD")
    range_low: int = Field(..., alias="rentRangeLow")
    range_high: int = Field(..., alias="rentRangeHigh")


class BaseEstimateParams(BaseModel):
    """Base parameters for property estimates (value or rent)."""
    address: str | None = Field(
        None,
        description="Full address in 'Street, City, State, Zip' format"
    )
    latitude: float | None = Field(
        None,
        description="Latitude of the property"
    )
    longitude: float | None = Field(
        None,
        description="Longitude of the property"
    )
    property_type: str | None = Field(
        None,
        alias="propertyType",
        description="Type of property"
    )
    bedrooms: float | None = Field(
        None,
        description="Number of bedrooms (use 0 for studio)"
    )
    bathrooms: float | None = Field(
        None,
        description="Number of bathrooms (supports fractions)"
    )
    square_footage: float | None = Field(
        None,
        alias="squareFootage",
        description="Total living area in square feet"
    )
    max_radius: float | None = Field(
        None,
        alias="maxRadius",
        description="Maximum search radius in miles"
    )
    days_old: int | None = Field(
        None,
        alias="daysOld",
        description="Maximum age of comparable listings in days"
    )
    comp_count: int | None = Field(
        None,
        alias="compCount",
        description="Number of comparable listings to return (5-25)",
        ge=5,
        le=25
    )


class ValueEstimateParams(BaseEstimateParams):
    """Parameters for requesting a property value estimate."""
    pass


class RentEstimateParams(BaseEstimateParams):
    """Parameters for requesting a property rent estimate."""
    property_type: str | None = Field(
        None,
        alias="propertyType",
        description="Type of property (Single Family, Condo, Townhouse, etc.)"
    )

    @field_validator('property_type', mode='before')
    @classmethod
    def validate_property_type(cls, v):
        if v and isinstance(v, str):
            try:
                return PropertyType(v.upper().replace(" ", "_"))
            except ValueError:
                return v
        return v

    def to_query_params(self) -> dict[str, str]:
        """Convert the model to query parameters for the API request."""
        params = {}
        for field_name, field in self.model_fields.items():
            value = getattr(self, field_name)
            if value is not None:
                # Convert enum values to their string representation
                if hasattr(value, 'value'):
                    value = value.value
                # Convert boolean to lowercase string
                elif isinstance(value, bool):
                    value = str(value).lower()
                # Convert other values to string
                else:
                    value = str(value)
                # Use the field's alias if available, otherwise use the field name
                param_name = field.alias or field_name
                params[param_name] = value
        return params