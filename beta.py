import datetime
from pandas_datareader import data
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def beta(datam,nikkei_df,s,e):
    selected = ["^NKX"]
    #株価データダウンロード
    #stooq = data.DataReader(selected,"stooq", start=s, end=e)
    stooq=nikkei_df
    data1 = stooq["Close"]

    data0=datam
    data1= pd.concat([data1,data0],axis=1).sort_values(by='Date',ascending=True)

    data2 = data1.pct_change()
    data3 = data2.iloc[::-1]
    data4 = data3.dropna()

    x = data4[selected[0]].values.reshape(-1,1)
    y = data4["Close"].values.reshape(-1,1)

    model_lr = LinearRegression()
    model_lr.fit(x,y)


    df1=stooq
    df2=data0

    df3=pd.DataFrame(df2["Close"] - df2["Close"].values.min()) / (df2["Close"].values.max() - df2["Close"].values.min())
    df4=pd.DataFrame(df1["Close"] - df1["Close"].values.min()) / (df1["Close"].values.max() - df1["Close"].values.min())

    #plt.figure(figsize=(12,4))
    #plt.title("Stock Price")
    #plt.xlabel("Date")
    #plt.ylabel("Price")
    #plt.grid(True)
#
    #plt.plot(df3, label="Prise")
    #plt.plot(df4, label="Nikkei")
    print(df3)
    #plt.legend()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df3.index,
                        y=df3.iloc[:,0],
                        mode='lines',
                        name='ポートフォリオ',
                        line=dict(color="#1c8dff")
                        )
              )
    fig.add_trace(go.Scatter(x=df4.index,
                    y=df4.iloc[:,0],
                    mode='lines',
                    name='日経平均',
                    line=dict(color="#ff8000")
                    )
            )
    fig.update_layout(xaxis=dict(title='日付'),
                  yaxis=dict(title='正規化株価'),
                  )
    fig.update_layout(
        plot_bgcolor='black',
        hovermode='x',
        width=800,
        height=500,
        legend=dict(xanchor='left',
                yanchor='bottom',
                x=0.02,
                y=0.9,
                orientation='h',
                )
        )
    return fig,'%.3f' %model_lr.coef_
    #print('%.3f' %model_lr.coef_)
