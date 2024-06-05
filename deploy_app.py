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
            'Date': scraped_data[0][1].text,
            'Open': float(scraped_data[0][2].text),
            'High': float(scraped_data[0][3].text),
            'Low': float(scraped_data[0][4].text),
            'Close': float(scraped_data[0][5].text),
            '%Change': scraped_data[0][6].text,
            'Change': float(scraped_data[0][7].text)
        }

        df = pd.DataFrame(data)
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict(df.iloc[0,['Open','High','Low','Close']])
        st.write(scraped_data)
        st.write(prediction)   


    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
