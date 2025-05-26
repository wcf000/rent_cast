"""
Common models and types used across the RentCast API client.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class PropertyType(str, Enum):
    """Enumeration of property types supported by the RentCast API."""
    SINGLE_FAMILY = "SINGLE_FAMILY"
    CONDO = "CONDO"
    TOWNHOUSE = "TOWNHOUSE"
    MULTI_FAMILY = "MULTI_FAMILY"
    APARTMENT = "APARTMENT"
    MANUFACTURED = "MANUFACTURED"
    LAND = "LAND"
    OTHER = "OTHER"


class OwnerType(str, Enum):
    """Enumeration of property owner types."""
    INDIVIDUAL = "Individual"
    BUSINESS = "Business"
    TRUST = "Trust"
    GOVERNMENT = "Government"
    OTHER = "Other"


class MailingAddress(BaseModel):
    """Mailing address model for property owner information."""
    id: str | None = Field(
        None,
        description="Unique identifier for the mailing address"
    )
    formatted_address: str = Field(
        ...,
        description="Full formatted mailing address"
    )
    address_line1: str = Field(..., description="Address line 1")
    address_line2: str | None = Field(None, description="Address line 2")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="2-letter state code")
    zip_code: str = Field(..., description="ZIP code")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "149-Weaver-Blvd,-264,-Weaverville,-NC-28787",
                "formatted_address": "149 Weaver Blvd, # 264, Weaverville, NC 28787",
                "address_line1": "149 Weaver Blvd",
                "address_line2": "# 264",
                "city": "Weaverville",
                "state": "NC",
                "zip_code": "28787"
            }
        }


class PropertyTaxYear(BaseModel):
    """Property tax information for a specific year."""
    year: int = Field(..., description="Year of the tax assessment")
    total: float = Field(..., description="Total tax amount in USD")


class PropertyHistoryEvent(BaseModel):
    """Historical event for a property (e.g., sale)."""
    event: str = Field(..., description="Type of event (e.g., 'Sale')")
    date: datetime = Field(..., description="Date of the event")
    price: float | None = Field(None, description="Price in USD, if applicable")


class PropertySearchParams(BaseModel):
    """Parameters for searching properties in the RentCast API."""
    address: str | None= Field(
        None,
        description="Full address in 'Street, City, State, Zip' format",
        examples=["5500 Grand Lake Dr, San Antonio, TX, 78244"]
    )
    city: str | None= Field(
        None,
        description="City name (case-sensitive)",
        examples=["San Antonio"]
    )
    state: str | None= Field(
        None,
        description="2-letter state code (case-sensitive)",
        examples=["TX"]
    )
    zip_code: str | None= Field(
        None,
        description="5-digit ZIP code",
        examples=["78244"]
    )
    latitude:float | None = Field(
        None,
        description="Latitude for area search",
        ge=-90,
        le=90
    )
    longitude:float | None = Field(
        None,
        description="Longitude for area search",
        ge=-180,
        le=180
    )
    radius:float | None = Field(
        None,
        description="Search radius in miles (max 100)",
        gt=0,
        le=100
    )
    property_type: PropertyType | None = Field(
        None,
        description="Type of property to filter by"
    )
    bedrooms:float | None = Field(
        None,
        description="Number of bedrooms (0 for studio)",
        ge=0
    )
    bathrooms:float | None = Field(
        None,
        description="Number of bathrooms (can be fractional)",
        gt=0
    )
    sale_date_range:int | None = Field(
        None,
        description="Max days since last sale (min 1)",
        ge=1
    )
    limit: int = Field(
        50,
        description="Number of results per page (1-500)",
        ge=1,
        le=500
    )
    offset: int = Field(
        0,
        description="Pagination offset",
        ge=0
    )

    @field_validator('state')
    @classmethod
    def validate_state_code(cls, v: str) -> str:
        if v and len(v) != 2:
            raise ValueError("State code must be 2 characters")
        return v.upper() if v else v

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: str) -> str:
        if v and not v.isdigit() or len(v) != 5:
            raise ValueError("ZIP code must be 5 digits")
        return v

    @field_validator('radius')
    @classmethod
    def validate_radius_with_coordinates(
        cls,
        v:float | None,
        info: FieldValidationInfo
    ) ->float | None:
        if v is not None and not any([
            info.data.get('latitude') is not None,
            info.data.get('address') is not None
        ]):
            raise ValueError(
                "Radius requires either latitude/longitude or address parameters"
            )
        return v

    def to_query_params(self) -> dict[str, str]:
        """Convert the model to query parameters for API requests."""
        params = {}
        for field_name, _field in self.model_fields.items():
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
                params[field_name] = value
        return params

RentCastBaseModel = BaseModel
