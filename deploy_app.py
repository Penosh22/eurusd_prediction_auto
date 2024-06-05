import streamlit as st
import pandas as pd
import pickle
import requests
from io import StringIO

def fetch_data():
    url = 'https://stooq.com/q/d/?s=eurusd'
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        st.write(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def parse_html(html_content):
    try:
        tables = pd.read_html(StringIO(html_content))  # Use StringIO to wrap the HTML content
        if tables:
            df = tables[0]
            df = df.dropna()
            return df
        else:
            st.write("No tables found in the HTML content.")
            return None
    except Exception as e:
        st.write(f"Error parsing HTML: {e}")
        return None

if st.button("Predict"):
    html_content = fetch_data()
    if html_content:
        df = parse_html(html_content)
        if df is not None:
            first_row = df.iloc[0]
            st.write(first_row)

            open_val = first_row['Open']
            high_val = first_row['High']
            low_val = first_row['Low']
            close_val = first_row['Close']
                    
            # Create a DataFrame with the values
            data = pd.DataFrame({
                'Open': [open_val],
                'High': [high_val],
                'Low': [low_val],
                'Close': [close_val]
            })

            with open('model.pkl', 'rb') as file:
                model = pickle.load(file)
            predictions = model.predict(data)
            st.write("Prediction:")
            st.write(predictions)
