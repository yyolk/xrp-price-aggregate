"""
Provides base classes for use along with ccxt.base.exchange.Exchange clients
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Union

import httpx

from ccxt.base import exchange  # type: ignore


class FakeCCXT(ABC):
    """
    ABC defining the interface we require for calling a bunch of ccxt
    clients.

    Implementing a class from this ABC allows you to call any API capable of
    returning a price to be considered in the aggregate.
    """

    # we should assume this client will be fast (use optimized endpoint)
    fast = True

    def __init__(self) -> None:
        # having an httpx client seems useful on the base class
        self.client = httpx.AsyncClient()

    @property
    @abstractmethod
    def id(self) -> str:  # pylint: disable=invalid-name
        """Returns the name of the exchange client

        This should return the name of the exchange we're fronting to
        conform to the ccxt-like client, it should also be lowered-case.
        """
        return "unknown"

    @classmethod
    @abstractmethod
    def price_to_precision(cls: Type[FakeCCXT], symbol: str, value: str) -> str:
        """Returns the value scaled based on the symbol's precision

        It's safe to return just the value if there is no mapping.
        """

    @abstractmethod
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """Return the results as a ccxt-like client would"""

    async def close(self) -> None:
        """Add any close logic here"""
        await self.client.aclose()


ExchangeClient = Union[FakeCCXT, exchange.Exchange]
