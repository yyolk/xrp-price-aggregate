from typing import Any, Dict

from .base import FakeCCXT


class Kraken(FakeCCXT):
    """
    Kraken has a public endpoint for fetching a price of a symbol.
    """

    fetch_ticker_url = "https://api.kraken.com/0/public/Ticker"

    @property
    def id(self) -> str:
        return "kraken"

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
        resp = await self.client.get(self.fetch_ticker_url, params={"pair": symbol})
        json_resp = resp.json()
        result = json_resp.get("result")
        price = result["XXRPZUSD"]["c"][0]
        return {"last": price}
