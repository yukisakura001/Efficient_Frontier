from pandas_datareader import data
import pandas as pd
from datetime import datetime,timedelta

def result(money,cor_list,weights,name):
    today = datetime.today().date()
    last_weekday = today - timedelta(days=10)
    df=data.DataReader(cor_list,"stooq",start=last_weekday,end=today)['Close'].head(1)
    list=df.values.tolist()[0]
    haibun=[i*int(money)*10000 for i in weights]
    stock=[int(a / b) for a, b in zip(haibun, list)]
    name_list=name["銘柄名"].values.tolist()
    stock_data=pd.DataFrame({"企業名":name_list,"購入株数":stock})
    result_df=stock_data.set_index("企業名")
    return result_df
