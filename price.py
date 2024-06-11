import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data
import plotly.graph_objects as go

def price(x,y,master_df):
    symbols=x
    bigger=y

    df=master_df
    # カラムを銘柄名でリネーム
    df.columns = symbols

    # 各銘柄の株価に重みをかけ、ポートフォリオの株価を計算
    #plt.clf()
    z = (df * bigger).sum(axis=1)
    z=z.to_frame(name='Close')
    z2=z.dropna()
    #fig, ax = plt.subplots(figsize=(12, 4))
    #ax.set_title("aa")
    #ax.set_xlabel("Date")
    #ax.set_ylabel("Price")
    #ax.grid(True)
    #ax.plot(z2["Close"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=z2.index,
                        y=z2["Close"],
                        mode='lines',
                        line=dict(color="#1c8dff")
                        )
              )
    fig.update_layout(xaxis=dict(title='日付'),
                  yaxis=dict(title='価格'),
                  )
    fig.update_layout(
        plot_bgcolor='black',
        width=800,
        height=600
        )
    return fig,z2
