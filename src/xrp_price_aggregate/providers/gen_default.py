from typing import List, Set, Tuple

import ccxt.async_support as ccxt  # type: ignore

from .base import ExchangeClient
from .binance import Binance
from .bitrue import Bitrue
from .kraken import Kraken


def generate_default() -> Tuple[Set[ExchangeClient], List[Tuple[ExchangeClient, str]]]:
    # get these popular, high volume exchanges from ccxt directly
    binance = ccxt.binance()
    bitfinex = ccxt.bitfinex()
    bitstamp = ccxt.bitstamp()
    cex = ccxt.cex()
    ftx = ccxt.ftx()
    # example where we could set a ccxt client as 'fast' directly, not really
    # intelligent, just empirical
    # setattr(ftx, "fast", True)
    hitbtc = ccxt.hitbtc()
    kraken = ccxt.kraken()
    # use our ccxt-like clients
    bitrue = Bitrue()
    binance2 = Binance()
    kraken2 = Kraken()
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
        binance2,
        kraken2,
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
        (binance2, "XRPUSDT"),
        (kraken2, "XRPUSD"),
    ]
    return exchanges, exchange_with_tickers


def generate_fast() -> Tuple[Set[ExchangeClient], List[Tuple[ExchangeClient, str]]]:
    """
    This will return the exchanges filtered from the default set if they have
    a `fast` attribute.
    """
    exchanges, exchange_with_tickers = generate_default()
    # set up our filter predicates
    filter_pred_fast_exchange_client = lambda exchange_client: hasattr(
        exchange_client, "fast"
    )
    filter_pred_fast_exchange_with_ticker = (
        lambda exchange_ticker: filter_pred_fast_exchange_client(exchange_ticker[0])
    )
    filtered_exchanges = set(filter(filter_pred_fast_exchange_client, exchanges))
    filtered_exchange_with_tickers = list(
        filter(filter_pred_fast_exchange_with_ticker, exchange_with_tickers)
    )
    return filtered_exchanges, filtered_exchange_with_tickers
