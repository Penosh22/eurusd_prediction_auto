import streamlit as st
import pandas as pd
import joblib
import pickle
import requests


# URL of the page to scrape
url = 'https://stooq.com/q/d/?s=eurusd'

# Send a GET request to the URL
response = requests.get(url)
if response.status_code == 200:
    tables = pd.read_html(response.text)
    if tables:
        df = tables[0].dropna()
        if not df.empty:
            # Proceed with the rest of the code if the DataFrame is not empty
            first_row = df.iloc[0]
            # ... rest of your code ...
        else:
            st.error("The DataFrame is empty after dropping NaN values.")
    else:
        st.error("No tables found on the webpage.")
else:
    st.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")

tables = pd.read_html(response.text)
table =tables[0]
df = table.dropna()



def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def make_predictions(model, data):
    predictions = model.predict(data)
    return predictions

def main():
    st.title("Model Deployment")

    model = load_model()

    # Get the first row of the eurusd_table_cleaned DataFrame
    # Get the first row of the DataFrame by position
    # first_row = df.iloc[0]


    # Assign the values to the variables
    open = first_row['Open']
    high = first_row['High']
    low = first_row['Low']
    close = first_row['Close']

    # Create a DataFrame with the values
    data = pd.DataFrame({
        'Open' : [open],
        'High' : [high],
        'Low' : [low],
        'Close' : [close]
    })

    # Display the values to the user
    st.write("Using the following data for prediction:")
    st.write(first_row)

    if st.button("Predict"):
        predictions = make_predictions(model, data)
        st.write("Prediction:")
        st.write(predictions)

if __name__ == "__main__":
    main()
