import pandas as pd
pd.set_option('display.max_columns', None)

df_all = pd.read_pickle('all_trades.pkl')
print(df_all.head())