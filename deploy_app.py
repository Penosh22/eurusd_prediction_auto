import streamlit as st
import pandas as pd
import pickle
import requests
from io import StringIO
from bs4 import BeautifulSoup
from tvDatafeed import TvDatafeed, Interval
st.title("EURUSD Prediction")
if st.button("predict"):
    tv = TvDatafeed()
    eur_usd_data = tv.get_hist(symbol='EURUSD', exchange='OANDA', interval=Interval.in_daily, n_bars=100)
    df =pd.DataFrame(eur_usd_data)
    data1 = {
        'Date1': df.iloc[-3].name,
        'Open1': df.iloc[-3]['open'],
        'High1': df.iloc[-3]['high'],
        'Low1': df.iloc[-3]['low'],
        'Close1': df.iloc[-3]['close']
    }
        
        
    data2 = {
        'Date2': df.iloc[-2].name,
        'Open2': df.iloc[-2]['open'],
        'High2': df.iloc[-2]['high'],
        'Low2': df.iloc[-2]['low'],
        'Close2': df.iloc[-2]['close']
    }
    data = {
        'Date': df.iloc[-2].name,
        'Open': df.iloc[-2]['open'],
        'High': df.iloc[-2]['high'],
        'Low': df.iloc[-2]['low'],
        'Close': df.iloc[-2]['close'],
        'Return': (data2['Close2']-data1['Close1'])/data1['Close1'],
        'Open_Close': data2['Close2']-data2['Open2'],
        'High_Low': data2['High2'] - data2['Low2'] if data2['Close2'] >= data2['Open2'] else data2['Low2'] - data2['High2']
    }


    df_predict = pd.DataFrame([data])
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    prediction = model.predict(df_predict[['Open','High','Low','Close','Return','Open_Close','High_Low']])
   
    st.write(data)
    st.write(data1,data2)
    st.write(prediction)   

        

        

