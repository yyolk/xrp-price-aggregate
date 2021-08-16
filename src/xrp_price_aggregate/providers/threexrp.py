"""
This will call the XRPL oracle to grab the price
"""
import asyncio
import json
import statistics
from decimal import Decimal
from typing import Dict

import websockets

from .base import FakeCCXT

# how long to listen to incoming messages for, if we keep this short, we can
# return a narrow window of all trades available to ThreeXRP
# in the future, we'll want to handle this more optimally giving all providers
# max time to do work with as many results as possible for aggregating
# LISTEN_FOR_SECONDS = 10
LISTEN_FOR_SECONDS = 1.337


class ThreeXRP(FakeCCXT):
    """
    Look up data that was persisted to the XRPL via the XRPL Oracles.
    """

    fast = False
    fetch_ticker_url = "wss://threexrp.dev"

    # def __init__(self) -> None:
    #     self.client = None

    @property
    def id(self) -> str:
        return "threexrp"

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
        async with websockets.connect(self.fetch_ticker_url) as websocket:  # type: ignore
            await websocket.send(
                json.dumps(
                    {
                        "request": "SUBSCRIBE",
                        "message": "threexrp v2 signin",
                        "channel": "trade",
                    }
                )
            )
            loop = asyncio.get_event_loop()
            start = loop.time()
            prices = []
            async for message in websocket:
                parsed_message = json.loads(message)
                trade = parsed_message.get("trade")
                if trade["f"] == symbol:
                    prices.append(Decimal(trade["p"]))
                    # we at least got one trade of the symbol we're looking for
                    if loop.time() - start > LISTEN_FOR_SECONDS:
                        break
            final_price = statistics.mean(prices)

        return {"last": str(final_price)}

    async def close(self) -> None:
        """We close exiting context_manager of our fetch_ticker client"""
        pass