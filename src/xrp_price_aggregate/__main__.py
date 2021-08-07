import sys

from . import as_json


# call with the fast parameter by default...
# ...unless provided with a short or long option
fast = not sys.argv[-1].endswith(("--exhaustive", "-E", "-L", "--long", "--ccxt"))

print(as_json(count=2, delay=0.25, fast=fast))
