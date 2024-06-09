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
        stop_level = 0
        # Iterate over each row in the table
        for row in table.find_all('tr'):
            # Extract the text from each cell in the row
            cells = [cell.text.strip() for cell in row.find_all('td')]
            # Append the list of cell values to the scraped_data list
            scraped_data.insert(0,cells)
            stop_level +=1
            if stop_level == 2:
                break
        
        data1 = {
            'Date1': scraped_data[0][1],
            'Open1': float(scraped_data[0][2]),
            'High1': float(scraped_data[0][3]),
            'Low1': float(scraped_data[0][4]),
            'Close1': float(scraped_data[0][5]),
            '%Change1': scraped_data[0][6],
            'Change1': float(scraped_data[0][7])
        }
        data2 = {
            'Date2': scraped_data[1][1],
            'Open2': float(scraped_data[1][2]),
            'High2': float(scraped_data[1][3]),
            'Low2': float(scraped_data[1][4]),
            'Close2': float(scraped_data[1][5]),
            '%Change2': scraped_data[1][6],
            'Change2': float(scraped_data[1][7])
        }
        data = {
            'Date': scraped_data[1][1],
            'Open': float(scraped_data[1][2]),
            'High': float(scraped_data[1][3]),
            'Low': float(scraped_data[1][4]),
            'Close': float(scraped_data[1][5]),
            'Return': (data2['Close2']-data1['Close1'])/data1['Close1'],
            'Open_Close': data2['Close2']-data2['Open2'],
            'High_Low': data2['High2'] - data2['Low2'] if data2['Close2'] >= data2['Open2'] else data2['Low2'] - data2['High2']
        }


        df = pd.DataFrame([data])
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict(df[['Open','High','Low','Close','Return','Open_Close','High_Low']])
       
        st.write(data)
        st.write(prediction)   


    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
