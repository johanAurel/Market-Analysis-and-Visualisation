import requests
import pandas as pd
from model.variables import URL, API_KEY
from model.model import indicator, support_and_resistance, plot_data, trading_signal



# Set up your API key and headers

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"  # Optional, based on API requirements
}

params ={
    'function':'TIME_SERIES_INTRADAY',
    'symbol':'EUR/USD',
    'interval':'60',
    'outputsize':'full'  # or 'compact' for less data
}

# Make the GET request
response = requests.get(URL, headers=headers, params=params)

# Check the status of the response
if response.status_code == 200:
    # Parse response as JSON
    data = response.json()  # Assuming the response is in JSON format
    
    # If data contains a nested dictionary or list, adjust accordingly
    # For example, if 'Time Series' is a key in the response:
    if 'Time Series' in data:
        # Extract time series data (assuming it is under the key 'Time Series')
        time_series_data = data['Time Series']

        # Convert time series data to DataFrame
        df = pd.DataFrame.from_dict(time_series_data, orient='index')

        # Display the first few rows
        print(df.head())

        # Print the columns of the DataFrame
        print(df.columns.tolist())
    else:
        print("Unexpected data structure:", data)
else:
    print(f"Error: {response.status_code}")
