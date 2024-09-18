from model.hidden import API_KEY,USER_ID
# Initialize all inputs to None
instrument = None
order = None
position = None
transaction = None
trade = None

# Function to get instrument input
def get_instrument():
    global instrument
    if instrument is None:
        instrument = input("Enter the instrument (e.g., 'USD_CAD'): ")
    return instrument

# Function to get order input
def get_order():
    global order
    if order is None:
        order = input("Enter the order (e.g: { price: 1.5000, stopLossOnFill: { timeInForce: GTC, price: 1.7000 },takeProfitOnFill: {price: 1.14530},timeInForce: GTC, instrument: USD_CAD,units: -1000,type: LIMIT,positionFill: DEFAULT})")
    return order

# Function to get position input
def get_position():
    global position
    if position is None:
        position = input("Enter the instrument for position (e.g., 'USD_CAD'): ")
    return position

# Function to get transaction ID input
def get_transaction():
    global transaction
    if transaction is None:
        transaction = input("Enter transaction ID (e.g., '6410'): ")
    return transaction

# Function to get trade ID input
def get_trade():
    global trade
    if trade is None:
        trade = input("Enter trade ID (e.g., '6459'): ")
    return trade

### OANDA API ###

# GET REQUESTS

# Accounts
LIST_OF_ACCOUNTS = 'https://api-fxpractice.oanda.com/v3/accounts'
FULL_DETAILS_OF_CHOSEN_ACCOUNT= f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}'
SUMMARY_OF_CHOSEN_ACCOUNT= f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/summary'

# Instruments
INSTRUMENTS_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/instruments'
CANDLES_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/instruments/{get_instrument()}/candles'

# Orders
ORDER_URL= f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/orders'
ORDER_SPECIFIER_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/orders/{get_order()}'
PENDING_ORDER_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/pendingOrders'

# Trades
LIST_OF_TRADES_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/trades'
OPEN_TRADES_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/openTrades'
GET_SPECIFIC_TRADES_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/trades/{get_trade()}'

# Positions
LIST_OF_POSITIONS_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/positions'
POSITIONS_FOR_SINGLE_INSTRUMENTS_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/positions/{get_position()}'
OPEN_POSITIONS_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/openPositions'

# Transactions
LIST_OF_ALL_TRANSACTION_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/transactions'
SINGLE_TRANSACTION_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/transactions/{get_transaction()}'

## POST REQUESTS ##

# Orders
CREATE_ORDER_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/orders'
create_order_header = {
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
    "Accept-Datetime-format": "RFC3339"
}
body = {
    # Fill this in with your order parameters as needed
}

# PUT REQUESTS

# Cancel an order
ORDER_CANCEL_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/orders/{get_order()}/cancel'

# Close a trade
TRADE_CLOSE_URL = f'https://api-fxpractice.oanda.com/v3/accounts/{USER_ID}/trades/{get_trade()}/close'

## Libraries to send

ACCOUNTS = {
    "GET": {
        'LIST_OF_ACCOUNTS': LIST_OF_ACCOUNTS, 
        'FULL_DETAILS_OF_CHOSEN_ACCOUNT' : FULL_DETAILS_OF_CHOSEN_ACCOUNT,
        'SUMMARY_OF_CHOSEN_ACCOUNT' : SUMMARY_OF_CHOSEN_ACCOUNT
    }
}

INSTRUMENTS = {
    "GET": {
        'INSTRUMENTS_URL': INSTRUMENTS_URL, 
        'CANDLES_URL': CANDLES_URL
    }
}

ORDERS = {
    "GET": {
        'ORDER_URL': ORDER_URL, 
        'ORDER_SPECIFIER_URL': ORDER_SPECIFIER_URL, 
        'PENDING_ORDER_URL': PENDING_ORDER_URL
    },
    "POST": {
        'CREATE_ORDER_URL': CREATE_ORDER_URL
    },
    "PUT": {
        'ORDER_CANCEL_URL': ORDER_CANCEL_URL
    }
}

TRADES = {
    "GET": {
        'LIST_OF_TRADES_URL': LIST_OF_TRADES_URL, 
        'OPEN_TRADES_URL': OPEN_TRADES_URL
    },
    "PUT": {
        'TRADE_CLOSE_URL': TRADE_CLOSE_URL
    }
}

POSITIONS = {
    "GET": {
        'LIST_OF_POSITIONS_URL': LIST_OF_POSITIONS_URL, 
        'POSITIONS_FOR_SINGLE_INSTRUMENTS_URL': POSITIONS_FOR_SINGLE_INSTRUMENTS_URL, 
        'OPEN_POSITIONS_URL': OPEN_POSITIONS_URL
    }
}

TRANSACTIONS = {
    "GET": {
        'LIST_OF_ALL_TRANSACTION_URL': LIST_OF_ALL_TRANSACTION_URL, 
        'SINGLE_TRANSACTION_URL': SINGLE_TRANSACTION_URL
    }
}
