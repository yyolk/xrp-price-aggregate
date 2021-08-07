from typing import List, Set, Tuple

import ccxt.async_support as ccxt  # type: ignore

from .base import ExchangeClient
from .binance import Binance
from .bitstamp import Bitstamp
from .bitrue import Bitrue
from .hitbtc import Hitbtc
from .kraken import Kraken


def generate_default() -> Tuple[Set[ExchangeClient], List[Tuple[ExchangeClient, str]]]:
    """
    Generates the default set of exchange clients and those clients with the
    pair should be called.

    The shape of this data is just what made sense at the time and is subject
    to change! :)


    Note on ``ExchangeClient.fast == True``:
        When giving an `ExchangeClient` the attribute of `fast = True` it will
        be considered in `generate_fast()` this is a rudimentary approach to
        giving this library some flexibility over aggregation of results from
        several sources, even if those sources may be duplicates of direct
        clients provided by ``ccxt``, the more ExchangeClients and pairs to
        call during aggregation seems useful as well, even if it is biasing the
        data those exchanges that are called, it is implicit these calls will
        be staggered over multiple loops of aggregation through ccxt's own
        `ccxt.base.exchange.Exchange` which has attached market data we're
        currently not utilizing, for the price aggregate function

        Some `ccxt.base.exchange.Exchange`s are faster than others, and can be
        considered to be included in the `generate_fast()` method by attaching
        the attribute directly:

            # example where we could set a ccxt client as 'fast' directly, not really
            # intelligent, just empirical through synthetic trials
            # setattr(ftx, "fast", True)

    """
    # get these popular, high volume exchanges from ccxt directly
    binance = ccxt.binance()
    bitfinex = ccxt.bitfinex()
    bitstamp = ccxt.bitstamp()
    cex = ccxt.cex()
    ftx = ccxt.ftx()
    hitbtc = ccxt.hitbtc()
    kraken = ccxt.kraken()
    # use our ccxt-like clients
    bitstamp2 = Bitstamp()
    bitrue = Bitrue()
    binance2 = Binance()
    kraken2 = Kraken()
    hitbtc2 = Hitbtc()
    # combine them all into a set for reference and iterating later
    exchanges = {
        binance,
        bitfinex,
        bitstamp,
        bitstamp2,
        cex,
        ftx,
        hitbtc,
        hitbtc2,
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
        (bitstamp2, "XRPUSD"),
        (bitstamp2, "XRPUSDT"),
        (cex, "XRP/USD"),
        (cex, "XRP/USDT"),
        (ftx, "XRP/USD"),
        (ftx, "XRP/USDT"),
        (hitbtc, "XRP/USDT"),
        (hitbtc2, "XRPUSDT"),
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
    filter_pred_fast_exchange_client = lambda exchange_client: (
        hasattr(exchange_client, "fast") and exchange_client.fast == True
    )
    filter_pred_fast_exchange_with_ticker = (
        lambda exchange_ticker: filter_pred_fast_exchange_client(exchange_ticker[0])
    )
    filtered_exchanges = set(filter(filter_pred_fast_exchange_client, exchanges))
    filtered_exchange_with_tickers = list(
        filter(filter_pred_fast_exchange_with_ticker, exchange_with_tickers)
    )
    return filtered_exchanges, filtered_exchange_with_tickers
