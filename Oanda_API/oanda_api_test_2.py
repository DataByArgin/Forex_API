import requests
import pandas as pd

import defs

session = requests.session()
instrument = 'EUR_USD'
count = 2
granularity = 'H1'

url = f'{defs.oanda_url}/instruments/{instrument}/candles'
params = dict(
    count = count,
    granularity = granularity,
    price = 'B'
)

response = session.get(url, params=params, headers=defs.header)
print(response.json())