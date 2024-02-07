import requests
import defs
import pandas as pd

session = requests.session()
instrument = 'EUR_USD'
count = 10
granularity = 'H1'
url = f'{defs.oanda_url}/instruments/{instrument}/candles'
params = dict(
    count = count,
    granularity = granularity,
    price = 'BMA'
)
response = session.get(url, params=params, headers=defs.header)
data = response.json()

prices = ['mid', 'bid', 'ask']
ohlc = ['o', 'h', 'l', 'c']
'''
for price in prices:
    for oh in ohlc:
        print(f'{price}_{oh}')
'''

our_data = []
for candle in data['candles']:
    if candle['complete'] == False:
        continue
    new_dict = {}
    new_dict['time'] = candle['time']
    new_dict['volume'] = candle['volume']
    for price in prices:
        for oh in ohlc:
            new_dict[f'{price}_{oh}'] = candle[price][oh]
    our_data.append(new_dict)
print(our_data[0])

candles_df = pd.DataFrame.from_dict(our_data)
print(candles_df)