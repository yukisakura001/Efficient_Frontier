# ライブラリの読み込み
from pandas_datareader import data
import pandas as pd
import datetime
#import matplotlib.pyplot as plt
import plotly.graph_objects as go

def nikkei(data0,start,end):
    df=data0
    df_sum=df.pct_change()
    cum_ret_d=(1+df_sum).cumprod()
    df_m = data.DataReader(["^NKX"],"stooq", start, end)
    df1=df_m['Close'].sort_index()
    df1_sum=df1.pct_change()
    cum_ret_d1=(1+df1_sum).cumprod()

    #fig=plt.figure(figsize=(12,4))
    #plt.plot(cum_ret_d,label="Price")
    #plt.plot(cum_ret_d1,label="Nikkei")
    #plt.xlabel("Date")
    #plt.ylabel("Price")
    #plt.grid(True)
    #plt.legend(loc = 'upper left')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cum_ret_d.index,
                        y=cum_ret_d["Close"],
                        mode='lines',
                        name='ポートフォリオ',
                        line=dict(color="#1c8dff")
                        )
              )
    fig.add_trace(go.Scatter(x=cum_ret_d1.index,
                    y=cum_ret_d1["^NKX"],
                    mode='lines',
                    name='日経平均',
                    line=dict(color="#ff8000")
                    )
            )
    fig.update_layout(xaxis=dict(title='日付'),
                  yaxis=dict(title='累積リターン'),
                  )
    fig.update_layout(
        plot_bgcolor='black',
        hovermode='x',
        width=800,
        height=600,
        legend=dict(xanchor='left',
                yanchor='bottom',
                x=0.02,
                y=0.9,
                orientation='h',
                )
        )
    return fig,df_m
