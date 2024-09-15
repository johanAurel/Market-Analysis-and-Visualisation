import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import requests as req
# from dotenv import load_dotenv
# import os



# load_dotenv()

# api_key = os.getenv('API_KEY')
# url = os.getenv('URL')


# params = {
#     'function': 'TIME_SERIES_INTRADAY',
#     'symbol': input("write symbol name"),   # Example symbol
#     'interval': input('Enter the interval (e.g., 5min):')  # Example interval
# }

# def choosing_stock(params):
#     # Print parameters to debug
#     print(f"Parameters received: {params}")
    
#     # Add API key to parameters
#     params['api_key'] = api_key
    
#     # Make API request
#     response = req.get(url, params=params)
    

#     if response.status_code == 200:
#         print('Success')
#         data = response.json()
#         # Print data to debug
#         print('Data received:', data)
#         # Assuming the API returns 'Time Series (Daily)'
#         if 'Time Series (Daily)' in data:
#             return pd.DataFrame(data['Time Series (Daily)']).T
#         else:
#             print('Expected data not found in the response.')
#             return None
#     else:
#         print(f'Error: {response.status_code}')
#         return None


# df = choosing_stock(params)

# # Print DataFrame to debug
# if df is not None:
#     print(df.head())
# else:
#     print("No data returned.")
print(pd.__version__)