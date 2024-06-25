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
        'Date1': df.tail(2)['datetime'].iloc[0],
        'Open1': df.tail(2)['open'].iloc[0],
        'High1': df.tail(2)['high'].iloc[0],
        'Low1': df.tail(2)['low'].iloc[0],
        'Close1': df.tail(2)['close'].iloc[0]
    }
        
        
    data2 = {
        'Date2': df.tail(2)['datetime'].iloc[1],
        'Open2': df.tail(2)['open'].iloc[1],
        'High2': df.tail(2)['high'].iloc[1],
        'Low2': df.tail(2)['low'].iloc[1],
        'Close2': df.tail(2)['close'].iloc[1]
    }
    data = {
        'Date': df.tail(2)['datetime'].iloc[1],
        'Open': df.tail(2)['open'].iloc[1],
        'High': df.tail(2)['high'].iloc[1],
        'Low': df.tail(2)['low'].iloc[1],
        'Close': df.tail(2)['close'].iloc[1],
        'Return': (data2['Close2']-data1['Close1'])/data1['Close1'],
        'Open_Close': data2['Close2']-data2['Open2'],
        'High_Low': data2['High2'] - data2['Low2'] if data2['Close2'] >= data2['Open2'] else data2['Low2'] - data2['High2']
    }


    df = pd.DataFrame([data])
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    prediction = model.predict(df[['Open','High','Low','Close','Return','Open_Close','High_Low']])
   
    st.write(data)
    st.write(df.tail(2))
    #st.write(prediction)   

        

        
