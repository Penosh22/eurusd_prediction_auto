import streamlit as st
import pandas as pd
import pickle
import time

def load_model():
    # Load the model from the serialized file
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def make_predictions(model, data):
    # Use the model to make predictions on the input data
    predictions = model.predict(data)
    return predictions

def main():
    st.title("EUR/USD Prediction Model Deployment")

    # Attempt to load the model
    try:
        model = load_model()
    except FileNotFoundError:
        st.error("Model file not found. Please ensure the model.pkl file exists.")
        return

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # URL of the page where the table is located
    url = 'https://stooq.com/q/d/?s=eurusd'

    # Retry until the DataFrame captures the table
    retry_count = 0
    max_retries = 5  # Set a maximum number of retries to prevent infinite loop
    while df.empty and retry_count < max_retries:
        try:
            # Use the read_html function to read tables from the webpage
            tables = pd.read_html(url)

            # Assuming the correct table is the second one (adjust the index accordingly)
            df = tables[1]  # Adjust the index accordingly

            # Clean the DataFrame by dropping rows with NaN values
            df = df.dropna()

            # Check if the DataFrame is still empty after cleaning
            if df.empty:
                raise ValueError("The DataFrame is empty after dropping NaN values.")

        except (ValueError, IndexError) as e:
            st.warning(f"Failed to load data. Retrying... ({retry_count + 1}/{max_retries})")
            time.sleep(5)  # Wait for 5 seconds before retrying
            retry_count += 1

    if retry_count == max_retries:
        st.error("Maximum number of retries reached. Unable to load data.")
        return

    # Proceed with the rest of the code if the DataFrame is not empty
    first_row = df.iloc[0]

    # Assign the values to the variables
    open_price = first_row['Open']
    high = first_row['High']
    low = first_row['Low']
    close = first_row['Close']

    # Create a DataFrame with the values
    data = pd.DataFrame({
        'Open': [open_price],
        'High': [high],
        'Low': [low],
        'Close': [close]
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
