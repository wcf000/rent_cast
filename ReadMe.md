# RentCast Python SDK

[![Python Version](https://img.shields.io/pypi/pyversions/rentcast-sdk)](https://pypi.org/project/rentcast-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, async Python SDK for the [RentCast API](https://rentcast.io/), providing type-safe access to real estate and rental market data.

## Features

- **Fully Typed**: Built with Python type hints and Pydantic for robust data validation
- **Async-First**: Leverages `asyncio` for high-performance concurrent requests
- **Comprehensive Coverage**: Supports all major RentCast API endpoints:
  - Property Data & Listings
  - Rental Market Data
  - Property Valuations
  - Market Statistics
- **Production Ready**: Includes retries, timeouts, and comprehensive error handling
- **Well-Tested**: 100% test coverage with a comprehensive test suite

## Installation

```bash
pip install rentcast-sdk
```

## Quick Start

```python
import asyncio
from rentcast import RentCastClient

async def main():
    # Initialize the client with your API key
    async with RentCastClient(api_key="your_api_key_here") as client:
        # Get property data by ID
        property_data = await client.property_data.get_by_id("12345")
        print(f"Property: {property_data.address}")
        
        # Search for rental listings
        listings = await client.listings.rental_listings(
            city="Austin",
            state="TX",
            limit=5
        )
        
        for listing in listings.data:
            print(f"${listing.price:,.0f} - {listing.bedrooms}bd/{listing.bathrooms}ba")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Client Initialization

```python
from rentcast import RentCastClient

# Basic initialization
client = RentCastClient(api_key="your_api_key")

# With custom configuration
client = RentCastClient(
    api_key="your_api_key",
    base_url="https://api.rentcast.io/v1",  # Default
    timeout=30.0,  # Request timeout in seconds
    max_retries=3,  # Number of retries for failed requests
)

# Recommended: use as a context manager
async with RentCastClient(api_key="your_api_key") as client:
    # Your code here
    pass
```

### Available Modules

#### Property Data

```python
# Get property by ID
property_data = await client.property_data.get_by_id("12345")

# Search properties
search_results = await client.property_data.search(
    address="123 Main St",
    city="Austin",
    state="TX",
    zip_code="78704",
    limit=10,
    offset=0
)

# Get random property records
random_properties = await client.property_data.random_records(limit=5)
```

#### Listings

```python
# Get rental listings
rentals = await client.listings.rental_listings(
    city="Austin",
    state="TX",
    min_price=1000,
    max_price=3000,
    bedrooms_min=2,
    limit=10
)

# Get sale listings
sales = await client.listings.sale_listings(
    city="Austin",
    state="TX",
    min_price=200000,
    max_price=500000,
    property_type="Single Family",
    limit=10
)

# Get listing by ID
listing = await client.listings.rental_listing_by_id("listing_123")
sale = await client.listings.sale_listing_by_id("sale_456")
```

#### Market Data

```python
# Get market statistics
market_data = await client.market_data.get_statistics(
    city="Austin",
    state="TX",
    metrics=["medianRent", "medianPrice"],
    interval="monthly",
    start_date="2023-01-01",
    end_date="2023-12-31"
)

# Get price and rent trends
trends = await client.market_data.get_trends(
    zip_code="78704",
    property_type="Single Family"
)
```

#### Property Valuation

```python
# Get property valuation
valuation = await client.valuation.get_valuation(
    address="123 Main St",
    city="Austin",
    state="TX",
    zip_code="78704",
    bedrooms=3,
    bathrooms=2,
    square_feet=1800,
    lot_size=6000,
    year_built=2010,
    property_type="Single Family"
)

# Get rent estimate
rent_estimate = await client.valuation.get_rent_estimate(
    address="123 Main St",
    city="Austin",
    state="TX",
    zip_code="78704",
    bedrooms=3,
    bathrooms=2,
    square_feet=1800
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from rentcast.exceptions import (
    RentCastError,
    RentCastAPIError,
    RentCastAuthenticationError,
    RentCastRateLimitError,
    RentCastValidationError,
    RentCastNotFoundError
)

try:
    # Your API calls here
    pass
except RentCastAuthenticationError as e:
    print(f"Authentication failed: {e}")
except RentCastRateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after} seconds")
except RentCastValidationError as e:
    print(f"Invalid request: {e}")
except RentCastAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Configuration

### Environment Variables

You can configure the client using environment variables:

```bash
export RENTCAST_API_KEY=your_api_key_here
export RENTCAST_BASE_URL=https://api.rentcast.io/v1
export RENTCAST_TIMEOUT=30.0
export RENTCAST_MAX_RETRIES=3
```

### Logging

The SDK uses Python's built-in logging. To enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact support@rentcast.io.

## Acknowledgements

- [RentCast](https://rentcast.io/) for providing the API
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [httpx](https://www.python-httpx.org/) for async HTTP requests

---

*This SDK is not officially affiliated with RentCast. Use at your own risk.*