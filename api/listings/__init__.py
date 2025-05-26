"""
RentCast Listings API client module.

This module provides access to RentCast's property listing endpoints.
"""

from typing import Optional

from ..client import RentCastClient
from .sale import SaleListingsClient

__all__ = [
    "SaleListingsClient",
]


def get_sale_listings_client(
    client: Optional[RentCastClient] = None,
    **kwargs
) -> SaleListingsClient:
    """
    Get a SaleListingsClient instance.

    Args:
        client: Optional RentCastClient instance. If not provided, a new one will be created.
        **kwargs: Additional arguments to pass to RentCastClient if creating a new instance.

    Returns:
        SaleListingsClient: An instance of the SaleListingsClient.
    """
    from ..client import RentCastClient as _RentCastClient
    
    if client is None:
        client = _RentCastClient(**kwargs)
        
    return SaleListingsClient(client)
