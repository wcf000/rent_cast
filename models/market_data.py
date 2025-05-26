"""
RentCast Market Data Models.

This module contains Pydantic models for handling market data from the RentCast API.
"""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, HttpUrl, field_validator

# Enums
class MarketDataInterval(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"

class MarketDataMetric(str, Enum):
    MEDIAN_RENT = "medianRent"
    MEDIAN_PRICE = "medianPrice"
    PRICE_PER_SQFT = "pricePerSqft"
    PRICE_TO_RENT_RATIO = "priceToRentRatio"
    DAYS_ON_MARKET = "daysOnMarket"
    INVENTORY = "inventory"
    MONTHS_OF_SUPPLY = "monthsOfSupply"

# Base Models
class MarketDataPoint(BaseModel):
    """A single data point in a market data series."""
    date: date
    value: float
    count: Optional[int] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median: Optional[float] = None
    avg: Optional[float] = None

class MarketDataSeries(BaseModel):
    """A series of market data points for a specific metric and property type."""
    metric: MarketDataMetric
    property_type: str = Field(..., alias="propertyType")
    data: List[MarketDataPoint]
    
    class Config:
        populate_by_name = True

class MarketDataResponse(BaseModel):
    """Response model for market data queries."""
    city: str
    state: str
    county: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_types: List[str] = Field(..., alias="propertyTypes")
    metrics: List[MarketDataMetric]
    interval: MarketDataInterval
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    series: List[MarketDataSeries]
    
    class Config:
        populate_by_name = True