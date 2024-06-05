import streamlit as st
import pandas as pd
import joblib
import pickle
import asyncio
from pyppeteer import launch

# Function to create a headless browser with Pyppeteer
async def create_browser():
    browser = await launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    return browser

# Function to scrape the data
async def scrape_data(url):
    browser = await create_browser()
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector('table')  # Ensure the table is loaded
    content = await page.content()
    await browser.close()
    
    # Parse the content with pandas
    tables = pd.read_html(content)
    return tables

# Wrapper function to run asyncio tasks
def run_asyncio_task(task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(task)

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
    tables = run_asyncio_task(scrape_data(url))
    
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
