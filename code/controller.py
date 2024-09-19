import requests
import json
import pandas as pd
from model.variables import ACCOUNTS,INSTRUMENTS,ORDERS,TRADES,POSITIONS
from model.hidden import API_KEY
from model.model import indicator, support_and_resistance, plot_data, trading_signal

# Set up your API key and headers

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json" , # Optional, based on API requirements
    'Accept-Datetime-Format': 'RFC3339'
}

params={
    "count": 200,
    "granularity": "M15",
    "alignmentTimezone": "America/New_York",
    "includeFirst": False,
    "from": "2021-01-01T00:00:00Z",
    "units": 0.5
    
}


response_1 = requests.get(ACCOUNTS['GET']['LIST_OF_ACCOUNTS'], headers=headers)

# Check the status of the response_1
if response_1.status_code == 200:
    print('Welcome on your server')
    response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](), headers=headers, params=params)
    data = response_2.json()  # Assuming the response_1 is in JSON format   
    df= pd.DataFrame(data)
    columns_names = df.columns #gives columns names in daraframe 
    candles_stick = pd.DataFrame(df.iloc[:, 2]) #e.g {'complete': True, 'volume': 11, 'time': '2021-01-03T22:30:00.000000000Z', 'mid': {'o': '1.27358', 'h': '1.27372', 'l': '1.27358', 'c': '1.27362'}}
    print(candles_stick)
else:
    print(f"Error: {response_1.status_code}")

