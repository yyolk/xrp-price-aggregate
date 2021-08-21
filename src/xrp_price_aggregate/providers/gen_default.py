"""
TODO:
    - https://github.com/yyolk/xrp-price-aggregate/issues/13
"""
from functools import partial
from typing import Callable, List, Set, Tuple

import ccxt.async_support as ccxt  # type: ignore

from .base import ExchangeClient
from .binance import Binance
from .bitstamp import Bitstamp
from .bitrue import Bitrue
from .hitbtc import Hitbtc
from .kraken import Kraken
# from .threexrp import ThreeXRP
from .xrpl_oracle import XRPLOracle


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
    # threexrp = ThreeXRP()
    xrpl_oracle = XRPLOracle()
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
        # threexrp,
        xrpl_oracle,
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
        # (threexrp, "USD"),
        (xrpl_oracle, "USD"),
    ]
    return exchanges, exchange_with_tickers


def _filter_on_client_attr(attr: str) -> Callable[[ExchangeClient], bool]:
    return lambda exchange_client: getattr(exchange_client, attr, False) is True


def _filter_gen(
    exchange_client_fpred: Callable[[ExchangeClient], bool],
    exchange_with_ticker_fpred: Callable[[Tuple[ExchangeClient, str]], bool],
) -> Tuple[Set[ExchangeClient], List[Tuple[ExchangeClient, str]]]:
    exchanges, exchange_with_tickers = generate_default()
    filtered_exchanges = set(filter(exchange_client_fpred, exchanges))
    filtered_exchange_with_tickers = list(
        filter(exchange_with_ticker_fpred, exchange_with_tickers)
    )
    return filtered_exchanges, filtered_exchange_with_tickers


# class ProviderFactory:
#     """A Factory of Providers
#
#     To replace gen_default, while retaining a glob-like approache to all
#     available exchanges with toggles on those clients for filtering what is
#     added in.
#     """
#
#     def __init__(self, exchange_client_fpred, exchange_with_ticker_fpred):
#         self.exchange_client_fpred = exchange_client_fpred
#         self.exchange_with_ticker_fpred = exchange_client_fpred

filter_pred_fast_exchange_client = _filter_on_client_attr("fast")
filter_pred_non_oracle_client: Callable[[Tuple[ExchangeClient, str]], bool] = (
    lambda exchange_client: not getattr(exchange_client, "xrpl_oracle", False) is True
)


generate_fast = partial(
    _filter_gen,
    filter_pred_fast_exchange_client,
    lambda exchange_ticker: filter_pred_fast_exchange_client(exchange_ticker[0]),
)

generate_oracle = partial(
    _filter_gen,
    filter_pred_non_oracle_client,
    lambda exchange_ticker: filter_pred_non_oracle_client(exchange_ticker[0]),
)
