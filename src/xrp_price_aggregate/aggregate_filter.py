import asyncio
import json
import logging
import statistics

from decimal import Decimal
from typing import Any, Awaitable, Callable, Dict, List, Set, Tuple

from .providers import ExchangeClient, generate_default


logger = logging.getLogger(__name__)
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logger.addHandler(logging.NullHandler())


def default_for_decimal(obj: Any) -> str:
    """handle Decimal, make a str"""
    if isinstance(obj, Decimal):
        return _format_decimal_result(obj)
    raise TypeError


def _format_decimal_result(result: Decimal) -> str:
    """When displaying a result, format to 5 significant digits"""
    return f"{result:.5f}"


def _format_decimal_results(results: List[Decimal]) -> List[str]:
    """Handles formatting multiple results"""
    return [_format_decimal_result(r) for r in results]


async def _async_get_price(exchange: ExchangeClient, pair: str) -> Tuple[str, Decimal]:
    """Utility function for grabbing the price from an exchange

    Args:
        exchange (ExchangeClient): A ccxt-like client
        pair (str): A pair like XRP/USD XRPUSD

    Returns:
        str: The exchange's id or name
        Decimal: The fetched price
    """
    ticker = await exchange.fetch_ticker(pair)
    return exchange.id, Decimal(
        exchange.price_to_precision(
            pair,
            # "last" is an alias to "close"
            ticker.get("last"),
        )
    )


async def _aggregate_multiple(count: int, delay: int) -> Dict[str, Any]:
    """Handles the aggregate workflow

    Handles the aggregate workflow, given a count and delay for cycling through
    our scoped tasks_fn, which uses the generated_default exchanges from this
    package for processing.

    Args:
        count (int): How many times to request from all providers
        delay (int): How long to wait after finishing all provider requests
                     before repeating

    Returns:
        Dict of [str, Any]: The aggregate results
    """
    exchanges: Set[ExchangeClient]
    exchange_with_tickers: List[Tuple[ExchangeClient, str]]
    exchanges, exchange_with_tickers = await generate_default()
    tasks_fn: Callable[[], List[Awaitable[Tuple[str, Decimal]]]] = lambda: [
        _async_get_price(exchange, ticker) for exchange, ticker in exchange_with_tickers
    ]
    try:
        all_results = []
        for _ in range(count):
            all_results += await asyncio.gather(*tasks_fn())
            # don't delay when calling once
            if count != 1:
                await asyncio.sleep(delay)

        raw_results = [raw_result for _, raw_result in all_results]
        # set up our container for named results
        raw_results_named: Dict[str, List] = {
            exchange.id: list() for exchange in exchanges
        }
        # fill our container with named results
        for exchange_name, raw_result in all_results:
            raw_results_named[exchange_name].append(raw_result)

        raw_stdev = statistics.stdev(raw_results)
        raw_median = statistics.median(raw_results)

        raw = {
            "raw_results_named": raw_results_named,
            "raw_results": raw_results,
            "raw_median": raw_median,
            "raw_stdev": raw_stdev,
        }
        logging.debug("raw is %s", raw)

        filtered_results = list(
            filter(
                # take the result subtracted from the median if it's lower
                # than the standard deviation
                lambda result: abs(result - raw_median) < raw_stdev,
                raw_results,
            )
        )
        filtered_median = statistics.median(filtered_results)
        filtered_mean = statistics.mean(filtered_results)
        filtered = {
            "filtered_results": filtered_results,
            "filtered_median": filtered_median,
            "filtered_mean": filtered_mean,
        }
        logging.debug("filtered is %s", filtered)

        return {
            **raw,
            **filtered,
        }
    finally:
        # we have no return, this is run "on the way out"
        close_exchanges_tasks = [exchange.close() for exchange in exchanges]
        # shield in case we are timed out, so the clients are closed
        await asyncio.shield(asyncio.gather(*close_exchanges_tasks))


def _compute_timeout(count: int, delay: int) -> int:
    """dumb logic for a max timeout, this could be better

    dumb logic for a max timeout, this could be better


    max_tasks_fn_timeout is 10 seconds and is the anticipated amount of time to
    do all concurrent requests in the workflow's (see ``tasks_fn``)

    """
    max_tasks_fn_timeout = 15
    return (count * max_tasks_fn_timeout) + (delay * count)


async def as_awaitable_json(count=1, delay=1) -> str:
    return json.dumps(
        await asyncio.wait_for(
            _aggregate_multiple(count, delay),
            timeout=_compute_timeout(count, delay),
        ),
        default=default_for_decimal,
    )


async def as_awaitable_dict(count=1, delay=1) -> Dict[str, Any]:
    return await asyncio.wait_for(
        _aggregate_multiple(count, delay), timeout=_compute_timeout(count, delay)
    )


def as_json(count=1, delay=1) -> str:
    return asyncio.run(as_awaitable_json(count, delay))


def as_dict(count=1, delay=1) -> Dict[str, Any]:
    return asyncio.run(as_awaitable_dict(count, delay))
