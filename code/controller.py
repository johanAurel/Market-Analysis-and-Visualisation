import requests
import time
import sys
import questionary
from model.variables import ACCOUNTS, INSTRUMENTS, ORDERS, TRADES, POSITIONS
from model.hidden import API_KEY, USER_ID
from model.model import trade_single_instrument_continuous, trade_all_instruments_continuous

# Set up your API key and headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    'Accept-Datetime-Format': 'RFC3339',
    'accountID': USER_ID
}

params = {
    "count": 250,
    "granularity": "M15",
    "alignmentTimezone": "America/New_York",
    "includeFirst": False,
    "from": "2025-07-01T00:00:00Z",
    "price": "M"
}

def is_interactive():
    return sys.stdin.isatty()

def fetch_candles(instrument, params=params, headers=headers):
    url = INSTRUMENTS['GET']['CANDLES'](instrument)
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("candles", [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

def run_trade():
    instrument = 'XPD_USD'
    trade_amount = 90.0
    strategy_name = 'ORB'
    print(f"Started monitoring {instrument} using {strategy_name}... Press Ctrl+C to stop.")
    trade_single_instrument_continuous(trade_amount, instrument, headers, strategy_name)

def action():
    instrument_name = ['XPD_USD', 'EUR_USD', 'JP225_JPY', 'XAU_USD', 'CH20_CHF', 'US30_USD', 'NATGAS_USD', 'US2000_USD']
    interactive = is_interactive()

    choice_1 = 'Trade' if not interactive else questionary.select(
        'What do you want to do?', choices=['See', 'Trade', 'Account', 'Exit']
    ).ask() or 'Exit'

    if choice_1 == 'See':
        sight = 'Trades' if not interactive else questionary.select(
            'What do you want to see?', choices=['Orders', 'Positions', 'Trades', 'Back']
        ).ask() or 'Back'

        if sight == 'Orders':
            res = requests.get(ORDERS['GET']['ORDER_URL'], headers=headers, params=params)
            print(res.json())
        elif sight == 'Positions':
            res = requests.get(POSITIONS['GET']['LIST_OF_POSITIONS_URL'], headers=headers, params=params)
            print(res.json())
        elif sight == 'Trades':
            res = requests.get(TRADES['GET']['LIST_OF_TRADES_URL'], headers=headers, params=params)
            for trade in res.json().get('trades', []):
                print(trade)
        action()

    elif choice_1 == 'Trade':
        choice_2 = 'Single-trade' if not interactive else questionary.select(
            'How do you want to trade?', choices=['Single-trade', 'Auto-trade', 'Close-All-Positions', 'Back']
        ).ask() or 'Back'

        if choice_2 == 'Single-trade':
            run_trade()

        elif choice_2 == 'Auto-trade':
            amount = 100.0 if not interactive else float(input('Choose a lot size for all trades: '))
            strategy_name = 'ORB' if not interactive else questionary.select(
                'Choose strategy:', choices=['ORB', 'VWAP']
            ).ask() or 'ORB'
            print(f"Auto-trading all instruments using {strategy_name}... Press Ctrl+C to stop.")
            trade_all_instruments_continuous(amount, instrument_name, headers, strategy_name)

        elif choice_2 == 'Close-All-Positions':
            print('Closing all positions...')
            for instrument in instrument_name:
                body = {"longUnits": "ALL", "shortUnits": "ALL"}
                try:
                    response = requests.put(POSITIONS['PUT'](instrument), headers=headers, json=body)
                    if response.status_code == 200:
                        print(f"✅ Closed position for {instrument}")
                    else:
                        print(f"❌ Failed to close {instrument}: {response.status_code} {response.text}")
                except Exception as e:
                    print(f"⚠️ Error closing {instrument}: {e}")
            action()
        else:
            action()

    elif choice_1 == 'Account':
        choice_3 = 'My details' if not interactive else questionary.select(
            'Account options:', choices=['My details', 'List of Accounts', 'Back']
        ).ask() or 'Back'

        if choice_3 == 'My details':
            opt = 'Summary' if not interactive else questionary.select(
                'Details view:', choices=['Summary', 'Full Details']
            ).ask() or 'Summary'
            url = ACCOUNTS['GET']['SUMMARY_OF_CHOSEN_ACCOUNT'] if opt == 'Summary' else ACCOUNTS['GET']['FULL_DETAILS_OF_CHOSEN_ACCOUNT']
            res = requests.get(url, headers=headers)
            print(res.json())
            time.sleep(5)
            action()

        elif choice_3 == 'List of Accounts':
            res = requests.get(ACCOUNTS['GET']['LIST_OF_ACCOUNTS'], headers=headers)
            accounts = [acc['id'] for acc in res.json().get('accounts', [])]
            _ = 'Back' if not interactive else questionary.select('Choose account:', choices=accounts).ask() or 'Back'
            time.sleep(2)
            action()
        else:
            action()

    else:
        print('Thank you, see you later!')

if __name__ == "__main__":
    try:
        print('📈 Autotrading running')
        while True:
            action()
    except KeyboardInterrupt:
        print("\n📉 Shutting down analysis.")
