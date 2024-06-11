from pandas_datareader import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

#cop_list1=["3407.JP","7453.JP","5021.JP","6504.JP","8035.JP","8830.JP","3626.JP","4062.JP","3861.JP","4206.JP"]
def eff(cop_list, start1, end1,label):
    start=start1
    end=end1
    symbols = cop_list
    master_df = data.DataReader(symbols,"stooq",start,end)['Close'].sort_index()

    df_day= master_df.pct_change()

    returns_annual = df_day.mean()*245

    cov_annual=df_day.cov()*245

    num=100000
    np.random.seed(0)

    port_returns = []
    port_volatility = []
    stock_weights = []
    sharpe_ratio = []

    # 様々な銘柄の比率でのポートフォリオのリターンとリスクを計算
    for i in range(num): # single_portfolio

        # 銘柄の比率を乱数で決定
        weights = np.random.uniform(1,10000,len(symbols))
        weights=weights**5
        weights /= np.sum(weights)

        # ポートフォリオの期待リターンを計算
        returns = np.dot(weights, returns_annual)

        # ポートフォリオのボラティリティを計算
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))

        # シャープレシオを計算
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)

        # 計算値をリストに格納
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    # 辞書型に格納
    portfolio = {"Returns": port_returns,
                "Volatility": port_volatility,
                "Sharpe Ratio" : sharpe_ratio}

    # 計算したポートフォリオのリターンとリスクに、比率のデータを加える
    for counter,symbol in enumerate(symbols):
        portfolio[str(symbol) + " Weight"] = [Weight[counter] for Weight in stock_weights]
    df = pd.DataFrame(portfolio)
    # データフレーム完成

    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()

    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]

    sharpe_sort=sharpe_portfolio.iloc[:,3:].T
    sharpe_sort.sort_values(by=sharpe_sort.columns[0] ,ascending=False ,axis=0,inplace=True)

    min_sort=min_variance_port.iloc[:,3:].T
    min_sort.sort_values(by=min_sort.columns[0] ,ascending=False ,axis=0,inplace=True)

    # グラフパラメータ設定
    plt.rcParams.update(plt.rcParamsDefault)

    plt.rcParams["axes.labelcolor"] = 'white'
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['xtick.color'] = 'gray'
    plt.rcParams['ytick.color'] = 'gray'
    plt.rcParams['text.color'] = 'white'

    # グラフ領域設定
    fig = plt.figure(facecolor='white',figsize=(15,12),tight_layout="True")
    spec = gridspec.GridSpec(ncols=2, nrows=3,height_ratios=[1,0.5,0.5],width_ratios=[0.5,1])

    #　グラフに領域を割り当て
    ax1 =  fig.add_subplot(spec[0,:], title='Efficient Frontier  ( '+str(start) +" - "+str(end)+ " )")
    ax2 =  fig.add_subplot(spec[1,0], title='Sharpe_port' )
    ax3 =  fig.add_subplot(spec[2,0], title='Min_variance_port')
    ax4 =  fig.add_subplot(spec[1,1], title='Sharpe_port')
    ax5 =  fig.add_subplot(spec[2,1], title='Min_variance_port')
    fig.patch.set_facecolor('black')

    # フロンティア、シャープ最大値、ボラティリティ最小値の散布図
    df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',cmap='gnuplot2', edgecolors='black',alpha=1, ax=ax1)
    ax1.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=50)
    ax1.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=50 )

    for counter,stock in enumerate(symbols):

        volatility = np.sqrt(cov_annual.loc[stock,stock])
        ax1.scatter(x=volatility, y=returns_annual[stock], c='y', marker='*', s=100)
        ax1.annotate(stock, (volatility*1.005, returns_annual[stock]*0.995),size=12,color="white")

    # パイチャート1
    df_pie1=sharpe_portfolio.T.iloc[3:,:]
    df_pie1=df_pie1.sort_values(by=df_pie1.columns[0], axis=0, ascending=True, inplace=False)
    col1=[s.replace(' Weight', '') for s in df_pie1.index.tolist()]
    ax2.pie(df_pie1.iloc[:,0].tolist(), autopct="%1.1f%%",startangle=90)
    ax2.legend(col1,fontsize=10,  bbox_to_anchor=(0, 0.9))


    # パイチャート２
    df_pie2=min_variance_port.T.iloc[3:,:]
    df_pie2=df_pie2.sort_values(by=df_pie2.columns[0], axis=0, ascending=True, inplace=False)
    col2=[s.replace(' Weight', '') for s in df_pie2.index.tolist()]
    ax3.pie(df_pie2.iloc[:,0].tolist(), autopct="%1.1f%%",startangle=90)
    ax3.legend(col2,fontsize=10,  bbox_to_anchor=(0, 0.9))


    # 積み上げグラフの元データ
    df_all=(1+master_df.pct_change()).cumprod()

    # 積み上げグラフ１
    df_sharpe=df_all.loc[:,col1]
    for i in range(len(col1)):
        df_sharpe.iloc[:,i]=df_sharpe.iloc[:,i] * df_pie1.iloc[:,0].values[i]
    ax4.stackplot(df_sharpe.index, df_sharpe.values.T)
    ax4.tick_params(axis='x', labelrotation=45)

    # 積み上げグラフ２
    df_min=df_all.loc[:,col2]
    for i in range(len(col2)):
        df_min.iloc[:,i]=df_min.iloc[:,i] * df_pie2.iloc[:,0].values[i]
    ax5.stackplot(df_min.index, df_min.values.T)
    ax5.tick_params(axis='x', labelrotation=45)

    plt.tight_layout()
    df_sharpe = df.sort_values("Sharpe Ratio", ascending=True)
    df1=df_sharpe.tail(1)
    df1_2 = df1.rename(index={df1.index[0]: '最大シャープレシオ'})
    df_min = df.sort_values("Volatility", ascending=True)
    df2=df_min.head(1)
    df2_2=df2.rename(index={df2.index[0]: '最少分散ポートフォリオ'})
    dfdf=pd.concat([df1_2,df2_2], axis=0)

    if label=="最大シャープレシオ":
        ddff=df_sharpe.tail(1).drop(["Returns","Volatility","Sharpe Ratio"],axis=1)
    elif label=="最小リスク":
        ddff=df_min.head(1).drop(["Returns","Volatility","Sharpe Ratio"],axis=1)
    wights=[]
    for i in range(0,len(ddff.columns)):
        wights.append(round(ddff.iat[0,i],8))

    return plt,dfdf,wights,master_df

#df = data.DataReader("4206.JP","stooq","01/04/19","02/03/23")
#print(df)
#3407.JP,7453.JP,5021.JP,6504.JP,8035.JP,8830.JP,3626.JP,4062.JP,3861.JP,4206.JP
#a,s,d,f=eff(["3407.JP","7453.JP","5021.JP","6504.JP","8035.JP","8830.JP","3626.JP","4062.JP","3861.JP","4206.JP"],"01/04/19","02/03/23")
#a.show()
