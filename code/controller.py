import requests
import time
import pandas as pd
import questionary
from model.variables import ACCOUNTS,INSTRUMENTS,ORDERS,TRADES,POSITIONS
from model.hidden import API_KEY, set_user_id
from model.model import create_dataframe,run_strategies

# Set up your API key and headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json" , # Optional, based on API requirements
    'Accept-Datetime-Format': 'RFC3339'
}

params={
    "count": 250,
    "granularity": questionary.select('Timeframe : ', choices=['S5','S10','S15','S30','M1','M5','M10','M15','M30','H1','H4','D','W','M']).ask(),
    "alignmentTimezone": "America/New_York",
    "includeFirst": False,
    "from": "2021-01-01T00:00:00Z"  
}

def trade_one(instrument=None):
    trade_amount = float(input('Enter trade amount: '))
    print(f"Started monitoring {instrument} for signals... Press Ctrl+C to stop.")

    while True:
        response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](instrument), headers=headers, params=params)

        if response_2.status_code == 200:
            data_2 = response_2.json()
            df_2 = pd.DataFrame(data_2)
            candle_sticks = data_2.get("candles", [])
            print(f"Fetched {len(candle_sticks)} candles for {instrument}")

            if not candle_sticks:
                print(f"No candles found for {instrument}")
                return

            create_dataframe(candle_sticks)
            run_strategies(trade_amount, instrument, ORDERS['POST']['CREATE_ORDER_URL'], headers=headers)

        else:
            print(f"Failed to fetch data for {instrument}: {response_2.status_code}")
        
        time.sleep(60)  # wait one candle (adjust based on your granularity)


   
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
      
      choice_1 = questionary.select('What do you want to do?', choices =['See','Trade','Account','Exit']).ask()  
      #choosing between Plot and Trade
      #SEE
      if choice_1 == 'See':
          sight = questionary.select('What do you want to see?', choices =['Orders','Positions','Trades','Back']).ask()
          if sight == 'Orders':
              res = requests.get(ORDERS['GET']['ORDER_URL'],headers=headers, params=params)
              orders = res.json()
              print(orders)
          elif sight == 'Positions':
              pos = requests.get(POSITIONS['GET']['LIST_OF_POSITIONS_URL'], headers=headers, params=params)
              positions = pos.json()
              print(positions)
          elif sight == 'Trades':
              tr = requests.get(TRADES['GET']['LIST_OF_TRADES_URL'],headers=headers,params=params)
              trades = tr.json()
              print(trade for trade in trades['trades'])
          else:
              action()
      #TRADE
      elif choice_1 == 'Trade':
          choice_2 = questionary.select('How do you want to do trade?', choices =['Single-trade','Auto-trade','Close-All-Positions','Back']).ask()
         
          if choice_2.lower() == 'single-trade':
             instrument_name = questionary.select('What do you want to trade?', choices = instrument_names).ask()
             trade_one(instrument=instrument_name)

          elif choice_2.lower() == 'auto-trade':
             amount = input('choose a lot size for all trade:')
             print("Auto-trading all instruments. Monitoring for signals... Press Ctrl+C to stop.")
             while True:
                 for instrument in list_of_instrument:
                     element = instrument['name']
                     response_2 = requests.get(INSTRUMENTS['GET']['CANDLES_URL'](element), headers=headers, params=params)
                     time.sleep(1)
                     if response_2.status_code == 200:
                         data_2 = response_2.json()
                         df_2 = pd.DataFrame(data_2)
                         candle_sticks = data_2.get("candles", [])
                         #print(f"Fetched {len(candle_sticks)} candles for {instrument}")
                         if not candle_sticks:
                             print(f"No candles found for {instrument}")
                             return

          elif choice_2.lower() == 'close-all-positions':
              print('Closing all positions...')
              while True:
                  for instrument in list_of_instrument:
                      element = instrument['name']
                      body = {"longUnits": "ALL", "shortUnits": "ALL" }
                      try:
                          response_2 = requests.put(
                              POSITIONS['PUT'](element),
                              headers=headers,
                              json=body  # ← important!
                              )
                          if response_2.status_code == 200:
                                  print(f"✅ Successfully closed position for {element}")
                          else:
                                  print(f"❌ Failed to close position for {element}: {response_2.status_code}")
                                  print(response_2.text)

                      except Exception as e:
                                      print(f"⚠️ Error while closing position for {element}: {str(e)}")
                  break

          
              
      #ACCOUNT
      elif choice_1 == 'Account':
        choices_3 = questionary.select('what interests you with your account today?',choices=['My details', 'List of Accounts','Back']).ask()
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
        elif choices_3 == 'List of Accounts':
          response_2 = requests.get(ACCOUNTS['GET']['LIST_OF_ACCOUNTS'],headers=headers)
          data_2 = response_2.json()
          list_of_accounts = data_2['accounts']
          accounts = [account['id']for account in list_of_accounts]
          new_user_id = questionary.select('choose account:', choices = accounts).ask()
          set_user_id(new_user_id)
          time.sleep(2)
          action()
        else:
            action()
      #STOP
      else:
          print('Thank you, see you later!!!')
          
   
   else:
        
        print(f"Failed to fetch data for {instrument}: {response_2.status_code}")     



if __name__ == "__main__":
    try:
        print('Autotrading running')
        while True:
            action()
    except KeyboardInterrupt:
        print("\n📉 Shutting down analysis.")

