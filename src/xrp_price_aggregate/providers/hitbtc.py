"""
HitBTC optimized price endpoint provider
"""
from typing import Dict

from .base import FakeCCXT


class Hitbtc(FakeCCXT):
    """
    Hitbtc has a public endpoint for fetching a price of a symbol.
    """

    fetch_ticker_url_template = "https://api.hitbtc.com/api/2/public/ticker/{symbol}"

    @property
    def id(self) -> str:
        return "hitbtc"

    @classmethod
    def price_to_precision(cls, _, value: str) -> str:
        """We have no intelligence for precision in this client"""
        return value

    async def fetch_ticker(self, symbol: str) -> Dict[str, str]:
        """Grab the response from our endpoint

        Grab the response from our endpoint, return a dict with the expected
        key of "last"


        Args:
            symbol (str): The symbol to request from the endpoint, like XRPUSD

        Returns:
            Dict of [str, str]: The results in a shape that includes our
                                expected "last" key
        """
        resp = await self.client.get(
            self.fetch_ticker_url_template.format(symbol=symbol)
        )
        json_resp = resp.json()
        return {"last": json_resp.get("last")}
