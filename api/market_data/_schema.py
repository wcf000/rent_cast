"""
RentCast Market Data API Schemas.

This module contains Pydantic models for request/response validation
in the RentCast Market Data API.
"""
from __future__ import annotations

from datetime import date
from typing import list

from pydantic import BaseModel, Field, field_validator

from ...models.market_data import MarketDataInterval, MarketDataMetric


class MarketDataRequest(BaseModel):
    """Request schema for market data queries."""
    city: str | None = Field(
        None,
        description="City name (required if zip_code not provided)"
    )
    state: str | None = Field(
        None,
        description="Two-letter state code (required if zip_code not provided)"
    )
    zip_code: str | None = Field(
        None,
        alias="zipCode",
        description="ZIP code (required if city/state not provided)"
    )
    property_types: list[str] = Field(
        default_factory=list,
        alias="propertyTypes",
        description="list of property types to include"
    )
    metrics: list[MarketDataMetric] = Field(
        default_factory=list,
        description="list of metrics to retrieve"
    )
    interval: MarketDataInterval = Field(
        default=MarketDataInterval.MONTHLY,
        description="Time interval for the data points"
    )
    start_date: date = Field(
        ...,
        alias="startDate",
        description="Start date for the data range"
    )
    end_date: date = Field(
        ...,
        alias="endDate",
        description="End date for the data range"
    )

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: str | None, values: dict) -> str | None:
        if v is None and not (values.get('city') and values.get('state')):
            raise ValueError("Either zip_code or both city and state are required")
        return v
