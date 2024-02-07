# Imports
import json
import requests
import numpy as np
import pandas as pd
import time
import defs
# Pricing path (Pricing Endpoints)
pricing_path = f'/v3/accounts/{defs.account_id}/pricing'
# Function to get the Ask price and the Time
def get_ask_price(instrument):
    query = {'instruments': instrument}
    response = requests.get('https://' + defs.oanda_url + pricing_path, headers=defs.header, params=query)
    result = response.json()

    prices_str = result['prices'][0]['asks'][0]['price']
    prices = float(prices_str)

    time_str = result['time']
    time = pd.to_datetime(time_str)

    return time, prices

# print(get_ask_price('EUR_USD'))

from_time = time.mktime(pd.to_datetime('01/01/2019').timetuple())
to_time = time.mktime(pd.to_datetime('01/01/2020').timetuple())
history_query = {'from': str(from_time), 'to': str(to_time), 'granularity': 'D'}
instrument = 'EUR_USD'
candles_path = f'/v3/accounts/{defs.account_id}/instruments/{instrument}/candles'
response = requests.get('https://' + defs.oanda_url + candles_path, headers=defs.header, params=history_query)

def json_to_pandas(json):
    json_file = json.json()
    price_json = json_file['candles']
    times = []
    open_price, high_price, low_price, close_price = [], [], [], []

    for candle in price_json:
        times.append(candle['time'])
        open_price.append(float(candle['mid']['o']))
        high_price.append(float(candle['mid']['h']))
        low_price.append(float(candle['mid']['l']))
        close_price.append(float(candle['mid']['c']))

    dataframe = pd.DataFrame({'Open': open_price, 'High': high_price, 'Low': low_price,
                              'Close': close_price})
    dataframe.index = pd.to_datetime(times)
    return dataframe

EURUSD_df = json_to_pandas(response)
print(EURUSD_df.head())


