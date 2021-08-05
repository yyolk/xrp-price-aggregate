# xrp-price-aggregate

Based on [XRPL-Labs/XRP-Price-Aggregator](https://github.com/XRPL-Labs/XRP-Price-Aggregator)


# Usage

1. `pip install xrp-price-aggregate`

2. Run directly as a module or import and provide aggregation count (how many
   rounds) along with delay between each round.


       # run xrp_price_aggregate.__main__ and also beautify the results
       python -m xrp_price_aggregate | python -m json.tool
       {
           "raw_results_named": {
               "hitbtc": [
                   "0.72235"
               ],
               ...
           },
           "raw_results": [
               "0.72110",
               "0.72236",
               "0.72202",
               ...
           ],
           "raw_median": "0.72219",
           "raw_stdev": "0.00071",
           "filtered_results": [
               "0.72236",
               "0.72202",
               "0.72240",
               ...
           ],
           "filtered_median": "0.72236",
           "filtered_mean": "0.72219"
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
    >>> xrp_price_aggregate.as_json()
    '{"raw_results_named": {"cex": ["0.72039", "0.72136"], "hitbtc": ["0.72122"], "kraken": ["0.72132"], "bitfinex": ["0.72145"], "bitstamp": ["0.72047"], "bitrue": ["0.72122"], "binance": ["0.72150"], "ftx": ["0.72078", "0.72155"]}, "raw_results": ["0.72150", "0.72145", "0.72047", "0.72039", "0.72136", "0.72078", "0.72155", "0.72122", "0.72132", "0.72122"], "raw_median": "0.72127", "raw_stdev": "0.00043", "filtered_results": ["0.72150", "0.72145", "0.72136", "0.72155", "0.72122", "0.72132", "0.72122"], "filtered_median": "0.72136", "filtered_mean": "0.72137"}'
    >>> xrp_price_aggregate.as_dict(count=3, delay=2)
    {'raw_results_named': {'binance': [Decimal('0.721'), Decimal('0.7213'), Decimal('0.7211')], 'ftx': [Decimal('0.7208'), Decimal('0.720975'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.7208'), Decimal('0.720975')], 'bitfinex': [Decimal('0.7215'), Decimal('0.7215'), Decimal('0.72141')], 'hitbtc': [Decimal('0.720796'), Decimal('0.720796'), Decimal('0.720796')], 'bitstamp': [Decimal('0.72047'), Decimal('0.72047'), Decimal('0.72047')], 'bitrue': [Decimal('0.72081'), Decimal('0.72094'), Decimal('0.72111')], 'kraken': [Decimal('0.72132'), Decimal('0.72132'), Decimal('0.72132')], 'cex': [Decimal('0.72039'), Decimal('0.72136'), Decimal('0.72039'), Decimal('0.72136'), Decimal('0.72039'), Decimal('0.72136')]}, 'raw_results': [Decimal('0.721'), Decimal('0.7215'), Decimal('0.72047'), Decimal('0.72039'), Decimal('0.72136'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72081'), Decimal('0.7213'), Decimal('0.7215'), Decimal('0.72047'), Decimal('0.72039'), Decimal('0.72136'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72094'), Decimal('0.7211'), Decimal('0.72141'), Decimal('0.72047'), Decimal('0.72039'), Decimal('0.72136'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72111')], 'raw_median': Decimal('0.720975'), 'raw_stdev': Decimal('0.0003566360729171225136133563969'), 'filtered_results': [Decimal('0.721'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72081'), Decimal('0.7213'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72094'), Decimal('0.7211'), Decimal('0.7208'), Decimal('0.720975'), Decimal('0.720796'), Decimal('0.72132'), Decimal('0.72111')], 'filtered_median': Decimal('0.720975'), 'filtered_mean': Decimal('0.7209962777777777777777777778')}
    ```

# Note on Jupyter


When running in Jupyter notebooks, be sure to use
[`nest_asyncio`](https://github.com/erdewit/nest_asyncio)

```py
import nest_asyncio
import xrp_price_aggregate


nest_asyncio.apply()


agg_results = xrp_price_aggregate.as_dict(count=6, delay=3)
```

[**Public Colab Example Notebook**](https://colab.research.google.com/drive/1OyV4P6dMFy3kBhV7FQNBW0lwHekkwAI6),
backup of the `.ipynb` [as a Gist](https://gist.github.com/yyolk/c293b66cea913c5b6dc3939a7f38b8bd)

