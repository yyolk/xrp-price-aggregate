from abc import ABC, abstractclassmethod, abstractproperty, abstractmethod
from typing import Any, Dict, Union

import httpx

from ccxt.base.exchange import Exchange  # type: ignore


class FakeCCXT(ABC):
    """
    ABC defining the interface we require for calling a bunch of ccxt
    clients.

    Implementing a class from this ABC allows you to call any API capable of
    returning a price to be considered in the aggregate.
    """

    def __init__(self):
        # having an httpx client seems useful on the base class
        self.client = httpx.AsyncClient()

    @abstractproperty
    def id(self) -> str:
        return "Unknown"

    @abstractclassmethod
    def price_to_precision(cls, symbol, value) -> str:
        pass

    @abstractmethod
    async def fetch_ticker(self, symbol) -> Dict[str, Any]:
        pass

    async def close(self):
        await self.client.aclose()


ExchangeClient = Union[FakeCCXT, Exchange]
