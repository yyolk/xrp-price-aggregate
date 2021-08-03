# xrp-price-aggregate

Based on [XRPL-Labs/XRP-Price-Aggregator](https://github.com/XRPL-Labs/XRP-Price-Aggregator)


# Usage

1. `pip install`

2. Run directly as a module or import and provide aggregation count (how many
   rounds) along with delay between each round.

        # run xrp_price_aggregate.__main__ and also beautify the results
        python -m xrp_price_aggregate | python -m json.tool
        {
            "raw_results_named": {
                "bitstamp": [
                    "0.71477"
                ],
                ...
            },
            "raw_results": [
                "0.7146",
                ...
            ],
            "raw_median": "0.7146375",
            "raw_stdev": "0.2259129230993412844271423067",
            "filtered_results": [
                "0.71460",
                "0.71567",
                ...
            ],
            "filtered_median": "0.71468",
            "filtered_mean": "0.71439"
        }




    ```py
    >>> # await it yourself
    >>> import asyncio
    >>> import xrp_price_aggregate
    >>> asyncio.run(xrp_price_aggregate.as_awaitable_json())
    '{"raw_results_named": {"hitbtc": ["0.711729"], "binance": ["0.7131"], "bitrue": ["0.71292"], "bitfinex": ["0.7122"], "ftx": ["0.712675", "0.7126"], "kraken": ["0.71223"], "cex": ["0.71334", "0.7135"], "bitstamp": ["0.71328"]}, "raw_results": ["0.7131", "0.7122", "0.71328", "0.71334", "0.7135", "0.712675", "0.7126", "0.711729", "0.71223", "0.71292"], "raw_median": "0.7127975", "raw_stdev": "0.0005759840275563203497399309551", "filtered_results": ["0.71310", "0.71328", "0.71334", "0.71268", "0.71260", "0.71223", "0.71292"], "filtered_median": "0.71292", "filtered_mean": "0.71288"}'
    ```
    ```py
    >>> # synchronous is the default case
    >>> import xrp_price_aggregate
    >>> xrp_price_aggregate.as_dict()
    {'raw_results_named': {'hitbtc': [Decimal('0.720423')], 'kraken': [Decimal('0.72032')], 'bitrue': [Decimal('0.72003')], 'bitfinex': [Decimal('0.71992')], 'ftx': [Decimal('0.71995'), Decimal('0.7202')], 'cex': [Decimal('0.71961'), Decimal('0.71869')], 'bitstamp': [Decimal('0.71994')], 'binance': [Decimal('0.7203')]}, 'raw_results': [Decimal('0.7203'), Decimal('0.71992'), Decimal('0.71994'), Decimal('0.71961'), Decimal('0.71869'), Decimal('0.71995'), Decimal('0.7202'), Decimal('0.720423'), Decimal('0.72032'), Decimal('0.72003')], 'raw_median': Decimal('0.71999'), 'raw_stdev': Decimal('0.0005005397198136338821186646099'), 'filtered_results': ['0.72030', '0.71992', '0.71994', '0.71961', '0.71995', '0.72020', '0.72042', '0.72032', '0.72003'], 'filtered_median': '0.72003', 'filtered_mean': '0.72008'}
    ```

