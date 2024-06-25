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
    df = df.drop(df.tail(1).index)
    df.reset_index(inplace=True)
    data1 = {
        'Date1': df.iloc[-2]['datetime'],
        'Open1': df.iloc[-2]['open'],
        'High1': df.iloc[-2]['high'],
        'Low1': df.iloc[-2]['low'],
        'Close1': df.iloc[-2]['close']
    }
        
        
    data2 = {
        'Date2': df.iloc[-1]['datetime'],
        'Open2': df.iloc[-1]['open'],
        'High2': df.iloc[-1]['high'],
        'Low2': df.iloc[-1]['low'],
        'Close2': df.iloc[-1]['close']
    }
    data = {
        'Date': df.iloc[-1]['datetime'],
        'Open': df.iloc[-1]['open'],
        'High': df.iloc[-1]['high'],
        'Low': df.iloc[-1]['low'],
        'Close': df.iloc[-1]['close'],
        'Return': (data2['Close2']-data1['Close1'])/data1['Close1'],
        'Open_Close': data2['Close2']-data2['Open2'],
        'High_Low': data2['High2'] - data2['Low2'] if data2['Close2'] >= data2['Open2'] else data2['Low2'] - data2['High2']
    }


    df = pd.DataFrame([data])
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    prediction = model.predict(df[['Open','High','Low','Close','Return','Open_Close','High_Low']])
   
    st.write(data)
    st.write(df.tail())
    st.write(prediction)   

        

        
