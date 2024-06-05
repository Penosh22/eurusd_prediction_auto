import streamlit as st
import pandas as pd
import pickle
import requests
from io import StringIO
from bs4 import BeautifulSoup

def fetch_data():
    url = 'https://stooq.com/q/d/?s=eurusd'
    response = requests.get(url)
    if response.status_code == 200:
        st.write("Successfully fetched data from the website.")
        return response.text
    else:
        st.write(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        tbody = soup.find("tbody", {"id": "f13"})
        if tbody:
            st.write("Found tbody in HTML.")
            trs = tbody.find_all("tr")
            if trs:
                tds = trs[0].find_all("td")
                if len(tds) >= 7:
                    data = {
                        'Date': tds[1].text,
                        'Open': float(tds[2].text),
                        'High': float(tds[3].text),
                        'Low': float(tds[4].text),
                        'Close': float(tds[5].text),
                        'Change': tds[6].text
                    }
                    st.write("Extracted data from first row:")
                    st.write(data)
                    return data
                else:
                    st.write("Not enough data in the first row.")
                    return None
            else:
                st.write("No rows found in tbody.")
                return None
        else:
            st.write("Tbody not found in HTML content.")
            return None
    except Exception as e:
        st.write(f"Error parsing HTML: {e}")
        return None

if st.button("Predict"):
    html_content = fetch_data()
    if html_content:
        data_dict = parse_html(html_content)
        if data_dict:
            # Convert the dictionary to a DataFrame
            data = pd.DataFrame([data_dict])
            
            st.write("Data to be used for prediction:")
            st.write(data)

            try:
                with open('model.pkl', 'rb') as file:
                    model = pickle.load(file)
                predictions = model.predict(data[['Open', 'High', 'Low', 'Close']])
                st.write("Prediction:")
                st.write(predictions)
            except Exception as e:
                st.write(f"Error loading the model or making predictions: {e}")
