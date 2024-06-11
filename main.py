import streamlit as st
import pandas as pd
import eff
import matplotlib.pyplot as plt
import price
import nikkei
import beta
import result
import requests

#@st.cache
def df_get():
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    r = requests.get(url)
    with open('data_j.xls', 'wb') as output:
        output.write(r.content)
    cor_df = pd.read_excel("./data_j.xls", index_col=1)[["銘柄名"]]
    return cor_df
def cor(name,df):
    name_list=name
    base= pd.DataFrame({'銘柄名': []})
    base.index.name="コード"

    for i in name_list:
        x=i.replace(".JP","")
        df1=df.loc[df.index == int(x)]
        base=pd.concat([base,df1])
    return base

cor_df=df_get()
st.title("株式投資ポートフォリオ提案")

select=st.selectbox("企業名入力",cor_df['銘柄名'].to_list())
sel_button=st.button("企業追加")


if 'name1' not in st.session_state: # 初期化
    st.session_state['name1'] = ""

if sel_button:
    num=cor_df[cor_df["銘柄名"]==select].index[0]
    if st.session_state['name1'] == "":
       st.session_state['name1'] =str(num)+".JP,"
    elif st.session_state['name1'][-1] != ",":
        st.session_state['name1'] =st.session_state['name1']+","+str(num)+".JP,"
    else:
        st.session_state['name1'] =st.session_state['name1']+str(num)+".JP,"
    #st.write(f"{num}.JP")
name = st.text_input('証券コードをコンマ区切りで入力してください(例：xxxx.JP,yyyy.JP,zzzz.JP)',value=st.session_state['name1'])
st.session_state['name1'] = name


name_list=name.rstrip(',').split(",")
s=st.text_input('計測開始日を入力してください(mm/dd/yy)',value='01/01/20')
e=st.text_input('計測終了日を入力してください(mm/dd/yy)',value='01/01/23')
money=st.text_input('投資金額を入力してください(万)',value='100')
label=st.radio('ポートフォリオを選択してください',('最小リスク','最大シャープレシオ'))
button = st.button('計算開始')
if button==True:
    st.header('企業一覧')
    dfn=cor(name_list,cor_df)
    st.table(dfn)
    st.header('効率的フロンティア')
    plta,sharp,weight,df=eff.eff(name_list,s,e,label)
    st.write(sharp)
    st.pyplot(plta)
    st.header('ポートフォリオ平均株価')
    pltp,stock_data=price.price(name_list,weight,df)
    #st.pyplot(pltp)
    st.plotly_chart(pltp)
    st.header('日経平均との累積リターンの比較')
    pltn,nikkeidf=nikkei.nikkei(stock_data,s,e)
    st.plotly_chart(pltn)
    st.header("市場β値")
    pltb,beta1=beta.beta(stock_data,nikkeidf,s,e)
    st.text("市場β値："+beta1)
    st.subheader("日経平均株価との価格推移比較（正規化）")
    st.plotly_chart(pltb)
    st.header("購入株数")
    result_df=result.result(money,name_list,weight,dfn)
    st.table(result_df)
