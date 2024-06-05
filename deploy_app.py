import streamlit as st
import pandas as pd
import pickle
import requests
import time

# Load model function
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Fetch data function
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Parse HTML and extract data
def parse_html(html_content):
    try:
        tables = pd.read_html(html_content)
        if tables:
            df = tables[0].dropna()
            return df
        else:
            st.error("No tables found in the HTML content.")
            return None
    except ValueError as e:
        st.error(f"Error parsing HTML content: {e}")
        return None

# Main function
def main():
    st.title("EUR/USD Prediction")
    if st.button("Predict"):
        url = 'https://stooq.com/q/d/?s=eurusd'
        time.sleep(5)  # Replace wait with sleep

        html_content = fetch_data(url)
        if html_content:
            df = parse_html(html_content)
            if df is not None:
                first_row = df.iloc[0]
                st.write(first_row)

                open_val = first_row['Otwarcie']
                high_val = first_row['Najwyższy']
                low_val = first_row['Najniższy']
                close_val = first_row['Zamknięcie']

                # Create a DataFrame with the values
                data = pd.DataFrame({
                    'Open': [open_val],
                    'High': [high_val],
                    'Low': [low_val],
                    'Close': [close_val]
                })

                # Load model and make predictions
                model = load_model()
                predictions = model.predict(data)
                st.write("Prediction:")
                st.write(predictions)

if __name__ == "__main__":
    main()
