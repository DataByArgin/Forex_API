import pandas as pd
import utils
import plotly.graph_objects as go
import instruments

pair = 'CAD_CHF'
granularity = 'H1'
ma_list = [16,64]
i_pair = instruments.Instrument.get_instrument_by_name(pair)

df = pd.read_pickle(utils.get_his_data_filename(pair, granularity))
non_cols = ['time', 'volume']
mod_cols = [x for x in df.columns if x not in non_cols]
df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

df_ma = df[['time', 'bid_o', 'bid_h', 'bid_l', 'bid_c']].copy()
for ma in ma_list:
    df_ma[f'MA_{ma}'] = df_ma.bid_c.rolling(window=ma).mean()
df_ma.dropna(inplace=True)
df_ma.reset_index(drop=True, inplace=True)
df_ma['DIFF'] = df_ma.MA_16 - df_ma.MA_64
df_ma['DIFF_PREV'] = df_ma.DIFF.shift(1)

def is_trade(row):
    if  row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

df_ma['IS_TRADE'] = df_ma.apply(is_trade, axis=1)
df_trades = df_ma[df_ma.IS_TRADE!=0].copy()

df_trades['DELTA'] = (df_trades.bid_c.diff()/i_pair.pipLocation).shift(-1)
df_trades['GAIN'] = df_trades['DELTA']*df_trades['IS_TRADE']
print(df_trades['GAIN'].sum())

df_plot = df_ma.iloc[-60:].copy()
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df_plot.time, open=df_plot.bid_o, high=df_plot.bid_h, low=df_plot.bid_l, close=df_plot.bid_c,
    line=dict(width=1),
    opacity=1,
    increasing_fillcolor='#24A06B',
    decreasing_fillcolor='#CC2E3C',
    increasing_line_color='#2EC886',
    decreasing_line_color='#FF3A4C'
))
for ma in ma_list:
    col = f'MA_{ma}'
    fig.add_trace(go.Scatter(x=df_plot.time,
                         y=df_plot[col],
                         line=dict(width=2),
                         line_shape='spline',
                         name=col))
fig.update_layout(width=2200, height=1200,
                  margin=dict(l=10, r=10, b=10, t=10),
                  font=dict(size=10, color='#e1e1e1'),
                  paper_bgcolor='#1e1e1e',
                  plot_bgcolor='#1e1e1e')
fig.update_xaxes(
    gridcolor='#1f292f',
    showgrid=True, fixedrange=True, rangeslider=dict(visible=False)
)
fig.update_yaxes(
    gridcolor='#1f292f',
    showgrid=True
)
#fig.show()
