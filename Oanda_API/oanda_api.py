import requests
import pandas as pd
import defs
import utils


class OandaAPI:
    def __init__(self):
        self.session = requests.session()

    def fetch_instruments(self):
        url = f'{defs.oanda_url}/accounts/{defs.account_id}/instruments'
        response = self.session.get(url, params=None, headers=defs.header)
        return response.status_code, response.json()

    def get_instruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None

    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())

    def fetch_candles(self, pair_name, count, granularity):
        url = f'{defs.oanda_url}/instruments/{pair_name}/candles'
        params = dict(
            count=count,
            granularity=granularity,
            price='B'
        )
        response = self.session.get(url, params=params, headers=defs.header)
        return response.status_code, response.json()


if __name__ == '__main__':
    api = OandaAPI()
