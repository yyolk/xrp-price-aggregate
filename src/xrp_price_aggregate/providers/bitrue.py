from typing import Any, Dict


from .base import FakeCCXT


class Bitrue(FakeCCXT):
    fetch_ticker_url = "https://www.bitrue.com/api/v1/ticker/price"

    @property
    def id(self) -> str:
        return "bitrue"

    @classmethod
    def price_to_precision(cls, _, value) -> str:
        """We have no intelligence for precision in this client"""
        return value

    async def fetch_ticker(self, symbol) -> Dict[str, Any]:
        resp = await self.client.get(self.fetch_ticker_url, params={"symbol": symbol})
        json_resp = resp.json()
        return {
            # default to 0 seems intelligent since it'll definitely be filtered
            # out, but skew the raw, unfiltered results
            "last": json_resp.get("price", "0")
        }
