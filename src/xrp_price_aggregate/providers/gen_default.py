from typing import List, Set, Tuple

import ccxt.async_support as ccxt  # type: ignore

from .base import ExchangeClient
from .bitrue import Bitrue


async def generate_default() -> Tuple[
    Set[ExchangeClient], List[Tuple[ExchangeClient, str]]
]:
    # get these popular, high volume exchanges from ccxt directly
    binance = ccxt.binance()
    bitfinex = ccxt.bitfinex()
    bitstamp = ccxt.bitstamp()
    cex = ccxt.cex()
    ftx = ccxt.ftx()
    hitbtc = ccxt.hitbtc()
    kraken = ccxt.kraken()
    # use our ccxt-like clients
    bitrue = Bitrue()
    # combine them all into a set for reference and iterating later
    exchanges = {
        binance,
        bitfinex,
        bitstamp,
        cex,
        ftx,
        hitbtc,
        kraken,
        bitrue,
    }

    # this could be more intelligently created, but this literal mapping is
    # known pairs
    exchange_with_tickers = [
        (binance, "XRP/USDT"),
        (bitfinex, "XRP/USD"),
        (bitstamp, "XRP/USD"),
        (cex, "XRP/USD"),
        (cex, "XRP/USDT"),
        (ftx, "XRP/USD"),
        (ftx, "XRP/USDT"),
        (hitbtc, "XRP/USDT"),
        (kraken, "XRP/USD"),
        (bitrue, "XRPUSDT"),
    ]
    return exchanges, exchange_with_tickers
