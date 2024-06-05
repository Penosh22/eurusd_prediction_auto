import streamlit as st
import pandas as pd
import joblib
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Function to create a headless Selenium WebDriver
def create_webdriver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--disable-setuid-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver

# Function to scrape the data
def scrape_data(url):
    driver = create_webdriver()
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load
    
    # Scrape the data table from the page
    tables = pd.read_html(driver.page_source)
    driver.quit()  # Close the WebDriver
    return tables

# Load the model from the pickle file
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Make predictions using the loaded model
def make_predictions(model, data):
    predictions = model.predict(data)
    return predictions

# Main function to run the Streamlit app
def main():
    st.title("Model Deployment")

    # URL of the page to scrape
    url = 'https://stooq.com/q/d/?s=eurusd'
    st.write("Fetching data from:", url)

    # Scrape data from the URL
    tables = scrape_data(url)
    if tables:
        df = tables[0].dropna()
        if not df.empty:
            first_row = df.iloc[0]
            
            # Assign the values to the variables
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

            # Display the scraped data
            st.write("Using the following data for prediction:")
            st.write(first_row)

            # Load the model
            model = load_model()

            if st.button("Predict"):
                predictions = make_predictions(model, data)
                st.write("Prediction:")
                st.write(predictions)
        else:
            st.error("The DataFrame is empty after dropping NaN values.")
    else:
        st.error("No tables found on the webpage.")

if __name__ == "__main__":
    main()
