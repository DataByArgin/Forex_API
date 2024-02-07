import pandas as pd
import plotly.graph_objects as go
pd.set_option('display.max_columns', None)

ma_test_res = pd.read_pickle('ma_test_res.pkl')
all_trades = pd.read_pickle('all_trades.pkl')
ma_test_res = ma_test_res[['pair', 'num_trades', 'total_gain', 'mashort', 'malong']]
ma_test_res['CROSS'] = 'MA_' + ma_test_res.mashort.map(str) + '_' + ma_test_res.malong.map(str)
df_all_gains = ma_test_res.groupby(by=['CROSS', 'mashort', 'malong'], as_index=False)['total_gain'].sum()
df_all_gains.sort_values(by='total_gain', ascending=False, inplace=True)

for cross in df_all_gains.CROSS.unique():
    df_temp = ma_test_res[ma_test_res.CROSS==cross]
    total_p = df_temp.shape[0]
    n_good = df_temp[df_temp.total_gain>0].shape[0]

    # print(f'{cross:12} {n_good:4} {(n_good/total_p)*100:4.0f}%')

crosses = df_all_gains.CROSS.unique()[:3]
df_good = ma_test_res[(ma_test_res.CROSS.isin(crosses)) & (ma_test_res.total_gain>0)].copy()
our_pairs = list(df_good.pair.value_counts()[:9].index)

all_trades['CROSS'] = 'MA_' + ma_test_res.mashort.map(str) + '_' + ma_test_res.malong.map(str)
trades_cad_jpy = all_trades[(all_trades.CROSS=='MA_8_16') & (all_trades.PAIR=='GBP_JPY')].copy()
trades_cad_jpy['CUM_GAIN'] = trades_cad_jpy.GAIN.cumsum()
trades_cad_jpy.sort_values(by='time', ascending=False, inplace=True)

def plot_line(df_plot, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_plot.time,
        y=df_plot.CUM_GAIN,
        line=dict(width=2,color="#3d825f"),
        line_shape='spline',
        name=name,
        mode='lines'
        ))
    fig.update_layout(width=1000,height=400,
        margin=dict(l=15,r=15,b=10),
        font=dict(size=10,color="#e1e1e1"),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        title=name)
    fig.update_xaxes(
        linewidth=1,
        linecolor='#3a4a54',
        showgrid=False,
        zeroline=False
    )
    fig.update_yaxes(
        linewidth=1,
        linecolor='#3a4a54',
        showgrid=False,
        zeroline=False
    )
    fig.show()

plot_line(trades_cad_jpy, "CAD_JPY")