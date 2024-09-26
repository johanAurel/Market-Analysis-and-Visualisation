import requests
import time
import pandas as pd
import questionary
from model.variables import ACCOUNTS,INSTRUMENTS,ORDERS,TRADES,POSITIONS
from model.hidden import API_KEY, set_user_id
from model.model import create_dataframe,indicator, support_and_resistance, plot_combined_data,trading_signal

# Set up your API key and headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json" , # Optional, based on API requirements
    'Accept-Datetime-Format': 'RFC3339'
}

params={
    "count": 250,
    "granularity": 'M15',
    "alignmentTimezone": "America/New_York",
    "includeFirst": False,
    "from": "2021-01-01T00:00:00Z",
    
    
}

def plot_chart(instrument=None):

    response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](instrument), headers=headers, params=params)
  
    if response_2.status_code == 200:
  
        data_2 = response_2.json()  # Assuming the response is in JSON format
        df_2 = pd.DataFrame(data_2)
        print('Welcome on your server')
        candle_sticks = df_2.iloc[:, 2]
        create_dataframe(candle_sticks)  # Call your dataframe creation function
        indicator()  # Call your indicator function
        support_and_resistance()  # Call your support and resistance function
        plot_combined_data()
    else:
      print(f"Failed to fetch data for {instrument}: {response_2.status_code}")

def trade_one(instrument=None):
   response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](instrument), headers=headers, params=params)

   if response_2.status_code == 200:
       data_2 = response_2.json()  # Assuming the response is in JSON format
       df_2 = pd.DataFrame(data_2)
       print('Welcome on your server')
       candle_sticks = df_2.iloc[:, 2]
       create_dataframe(candle_sticks)  # Call your dataframe creation function
       indicator()  # Call your indicator function
       support_and_resistance()  # Call your support and resistance function
       trade_amount = float(input('Enter trade amount: '))
       trading_signal(trade_amount, instrument, ORDERS['POST']['CREATE_ORDER_URL'], headers=headers)
   else:
      print(f"Failed to fetch data for {instrument}: {response_2.status_code}")
      trade_one()

   
# Check the status of the response_1
def action():
   count = 0
   response_1 = requests.get(INSTRUMENTS['GET']['INSTRUMENTS_URL'], headers=headers, params=params)
   if response_1.status_code == 200:
      data_1 = response_1.json()
      df_1 = pd.DataFrame(data_1)
      print('Welcome on your server')
      list_of_instrument = df_1.iloc[:, 0]
      instrument_names = []

      for instrument in list_of_instrument:
         instrument_names.append(instrument['name'])
      
      choice_1 = questionary.select('What do you want to do?', choices =['Plot','Trade','Account','End']).ask()  
      #choosing between Plot and Trade
      #PLOT
      if choice_1.lower() == 'plot':
          instrument_name = questionary.select('What do you want to plot?', choices = instrument_names).ask()
          plot_chart(instrument=instrument_name)
      #TRADE
      elif choice_1.lower() == 'trade':
          choice_2 = questionary.select('How do you want to do trade?', choices =['Single-trade','Auto-trade']).ask()
         
          if choice_2.lower() == 'single-trade':
             instrument_name = questionary.select('What do you want to trade?', choices = instrument_names).ask()
             trade_one(instrument=instrument_name)

          elif choice_2.lower() == 'auto-trade':
             amount = input('choose a lot size for all trade:')
             while True:            
              for instrument in list_of_instrument:
                    element = instrument['name']
                               
                    response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](element), headers=headers, params=params)
                    time.sleep(1)

                    if response_2.status_code == 200: 
                               
                     data_2 = response_2.json()  # Assuming the response is in JSON format
                     df_2 = pd.DataFrame(data_2)
                     candle_sticks = df_2.iloc[:, 2]
                     create_dataframe(candle_sticks)  # Call your dataframe creation function
                     indicator()  # Call your indicator function
                     support_and_resistance()  # Call your support and resistance function
                     trading_signal(amount, element, ORDERS['POST']['CREATE_ORDER_URL'], headers=headers) # Call
                     count += 1
                     print(f'cycle count:{count}')
                    else:
                     print(f"Failed to fetch data for {instrument}: {response_2.status_code}")
          else: 
             action()        
      #ACCOUNT
      elif choice_1.lower() == 'account':
        choices_3 = questionary.select('what interests you with your account today?',choices=['My details', 'List of Accounts']).ask()
        if choices_3 == 'My details':
           options = questionary.select('', choices=['Summary', 'Full Details']).ask()
           if options == 'Summary':
              response_2 = requests.get(ACCOUNTS['GET']['SUMMARY_OF_CHOSEN_ACCOUNT'],headers=headers)
              data_2 = response_2.json()
              print(data_2)
              time.sleep(5)
              action()
           elif options == 'Full Details':
              response_2 =requests.get(ACCOUNTS['GET']['FULL_DETAILS_OF_CHOSEN_ACCOUNT'],headers=headers)
              data_2 = response_2.json()
              print(data_2)
              time.sleep(10)
              action()
        else:
          response_2 = requests.get(ACCOUNTS['GET']['LIST_OF_ACCOUNTS'],headers=headers)
          data_2 = response_2.json()
          list_of_accounts = data_2['accounts']
          accounts = [account['id']for account in list_of_accounts]
          new_user_id = questionary.select('choose account:', choices = accounts).ask()
          set_user_id(new_user_id)
          time.sleep(2)
          action()
      #STOP
      else:
          print('Thank you, see you later!!!')
          
   
   else:
        
        print(f"Failed to fetch data for {instrument}: {response_2.status_code}")     

action()

