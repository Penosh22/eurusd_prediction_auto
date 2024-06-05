import streamlit as st
import pandas as pd
import pickle
import requests
import time

if st.button("Predict"):
    url = 'https://stooq.com/q/d/?s=eurusd'
    response = request.get(url)
    if response.status_code == 200:
        tables =pd.read_html(response.text)
        df = tables[0]
        first_row = df.iloc[0]
        st.write(first_row)
    else:
        st.write(f"Failed to retrieve the webpage. Status code: {response.status_code}")

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
