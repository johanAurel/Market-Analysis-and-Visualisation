import requests
import pandas as pd
from model.variables import URL, API_KEY

# Define parameters for API request
params = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': 'EUR/USD',  # Example symbol, replace with actual if needed
    'interval': '5min',
    'apikey': API_KEY  # Correct parameter name for API key
}

def fetch_data():
    try:
        # Make the API request
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            key = f'Time Series ({params["interval"]})'  # Dynamic key based on interval

            # Debugging: print out the raw response to check data structure
            print("Raw data from API:", data)

            # Check if the key exists in the response
            if key in data:
                df = pd.DataFrame(data[key]).T  # Transpose to get time as index
                df.index = pd.to_datetime(df.index)  # Convert index to datetime
                df = df.astype(float)  # Convert data to float
                return df
            else:
                print(f"Key '{key}' not found in response.")
                return None
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Fetch data and create DataFrame
data_frame = fetch_data()
print(data_frame)
