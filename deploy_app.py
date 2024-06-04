import streamlit as st
import pandas as pd
import joblib
import pickle


import pandas as pd

# URL of the page where the table is located
url = 'https://stooq.com/q/d/?s=eurusd'

# Use the read_html function to read tables from the webpage
tables = pd.read_html(url)

# Inspect the tables list to find the correct table
# This step may require manual inspection. For example, if the correct table is the second one:
df = tables[1]  # Adjust the index accordingly

# Clean the DataFrame by dropping rows with NaN values
df = df.dropna()

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

'''
import streamlit as st
import pandas as pd
import joblib
import pickle

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

    open = st.number_input('Open', format="%.5f")
    high = st.number_input('High', format="%.5f")
    low = st.number_input('Low', format="%.5f")
    close = st.number_input('Close', format="%.5f")

    data = pd.DataFrame({
        'Open' : [open],
        'High' : [high],
        'Low' : [low],
        'Close' : [close]
    })

    if st.button("Predict"):
        predictions = make_predictions(model, data)
        st.write(predictions)

if __name__ == "__main__":
    main()
'''
