# import requests
import json
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
# response = requests.get(URL, headers=headers, params=params)

# # Check the status of the response
# if response.status_code == 200:
#     # Parse response as JSON
#     data = response.json()  # Assuming the response is in JSON format
#     df= pd.DataFrame(data)
#     columns_names = df.columns
#     print(df.head())


# else:
#     print(f"Error: {response.status_code}")

Dict = { "A":[1], "B":[2], "C": [3]}
df = pd.DataFrame(Dict)
print(df.head(2))