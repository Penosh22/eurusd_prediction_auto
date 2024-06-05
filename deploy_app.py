import streamlit as st
import pandas as pd
import pickle
import requests
from io import StringIO
from bs4 import BeautifulSoup

st.title("EURUSD Prediction")
if st.button("predict"):

    # URL of the page to scrape
    url = 'https://stooq.com/q/d/?s=eurusd'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with the data
        table = soup.find('tbody', {'style': 'background-color:ffffff'})
        
        # Initialize a list to store the scraped data
        scraped_data = []
        
        # Iterate over each row in the table
        for row in table.find_all('tr'):
            # Extract the text from each cell in the row
            cells = [cell.text.strip() for cell in row.find_all('td')]
            # Append the list of cell values to the scraped_data list
            scraped_data.append(cells)
            break
        
        data = {
            'Date': scraped_data[0][1],
            'Open': float(scraped_data[0][2]),
            'High': float(scraped_data[0][3]),
            'Low': float(scraped_data[0][4]),
            'Close': float(scraped_data[0][5]),
            '%Change': scraped_data[0][6],
            'Change': float(scraped_data[0][7])
        }

        df = pd.DataFrame([data])
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict(df[['Open','High','Low','Close']])
        st.write(data)
        st.write(prediction)   


    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
