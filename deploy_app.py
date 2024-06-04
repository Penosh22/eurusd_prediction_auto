import streamlit as st
import pandas as pd
import joblib
import pickle
import requests


# URL of the page to scrape
url = 'https://stooq.com/q/d/?s=eurusd'

# Send a GET request to the URL
response = requests.get(url)

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
    first_row = df.iloc[0]


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
