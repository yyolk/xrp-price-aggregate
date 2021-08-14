"""
This will call the XRPL oracle to grab the price
"""
import asyncio
import statistics
from decimal import Decimal
from typing import Dict

from .base import FakeCCXT


# see gravatar to understand ;)
XRPL_ORACLE__UNICORN_CAT = "r9PfV3sQpKLWxccdg3HL2FXKxGW2orAcLE"


class XRPLOracle(FakeCCXT):
    """
    Look up data that was persisted to the XRPL via the XRPL Oracles.
    """

    # assume mainnet
    fetch_ticker_url = "https://xrplcluster.com"
    # we might want other ways of reading this data
    xrpl_oracle = True

    @property
    def id(self) -> str:
        return "xrpl_oracle"

    @classmethod
    def price_to_precision(cls, _: str, value: str) -> str:
        """We have no intelligence for precision in this client"""
        return value

    async def fetch_ticker(self, symbol: str) -> Dict[str, str]:
        """Grab the response from our endpoint

        Grab the response from our endpoint, return a dict with the expected
        key of "last"


        Args:
            symbol (str): The symbol to request from the endpoint, like xrpusd

        Returns:
            Dict of [str, str]: The results in a shape that includes our
                                expected "last" key
        """
        successful = False
        # optimistically, the XRPL is always up and reachable, we may need to
        # add better logic for selecting more than one endpoint
        while not successful:
            resp = await self.client.post(
                self.fetch_ticker_url,
                json={
                    "method": "account_lines",
                    "params": [{"account": XRPL_ORACLE__UNICORN_CAT}],
                },
            )
            if resp.status_code == 200:
                successful = True
                json_resp = resp.json()
                trust_lines = json_resp["result"]["lines"]
                average = statistics.mean(
                    Decimal(trust_line["limit_peer"])
                    for trust_line in filter(lambda tl: tl["currency"] == symbol, trust_lines)
                )
            else:
                await asyncio.sleep(0.05)
        return {"last": str(average)}
