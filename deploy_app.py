import streamlit as st
import pandas as pd
import pickle
import requests

# Function to download the webpage content
def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('downloaded_page.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        st.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    return 'downloaded_page.html'

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

    # Download the webpage content
    file_path = download_page(url)
    
    if file_path:
        # Parse the HTML content with pandas
        tables = pd.read_html(file_path)
        
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
            st.error("No tables found in the downloaded HTML content.")

if __name__ == "__main__":
    main()
