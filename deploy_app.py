import streamlit as st
import pandas as pd
import pickle
import requests
from io import StringIO

url = 'https://stooq.com/q/d/?s=eurusd'
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    tables = pd.read_html(StringIO(html_content))  # Use StringIO to wrap the HTML content
    df = tables[0]
    df = df.dropna()
    first_row = df.iloc[0]
    st.write(df.head()) 
