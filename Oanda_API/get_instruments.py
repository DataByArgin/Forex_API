import requests
import pandas as pd
import defs

session = requests.session()
url = f'{defs.oanda_url}/accounts/{defs.account_id}/instruments'
response = session.get(url, params=None, headers=defs.header)
data = response.json()
instruments = data['instruments']

instrument_data = []
for item in instruments:
    new_obj = dict(
        name = item['name'],
        type = item['type'],
        displayName = item['displayName'],
        pipLocation = item['pipLocation'],
        marginRate = item['marginRate']
    )
    instrument_data.append(new_obj)

instrument_df = pd.DataFrame.from_dict(instrument_data)
instrument_df.to_pickle('instruments.pkl')
new_table = pd.read_pickle('instruments.pkl')
print(new_table)