import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# Initialize a global DataFrame variable
exportable_df = pd.DataFrame()

# Function to convert candlesticks array to a DataFrame
def create_dataframe(candlesticks):
    global exportable_df  # Declare that we're modifying the global DataFrame
    
    # Extract data from each candlestick and structure it into a DataFrame
    data = {
        'Date': [candle['time'] for candle in candlesticks],
        'Open': [float(candle['mid']['o']) for candle in candlesticks],
        'High': [float(candle['mid']['h']) for candle in candlesticks],
        'Low': [float(candle['mid']['l']) for candle in candlesticks],
        'Close': [float(candle['mid']['c']) for candle in candlesticks],
        'Volume': [candle['volume'] for candle in candlesticks]
    }

    # Create a DataFrame from the structured data
    exportable_df = pd.DataFrame(data)
    
    # Convert 'Date' to datetime format
    exportable_df['Date'] = pd.to_datetime(exportable_df['Date'])

    # Set 'Price' to be the 'Close' price for simplicity (this is used for VWAP)
    exportable_df['Price'] = exportable_df['Close']
    
    return exportable_df

# Function to calculate indicators
def indicator():
    global exportable_df  # Use the global DataFrame

    # Calculate moving averages
    exportable_df['MA50'] = exportable_df['Close'].rolling(window=50).mean()
    exportable_df['MA9'] = exportable_df['Close'].rolling(window=9).mean()
    exportable_df['MA5'] = exportable_df['Close'].rolling(window=5).mean()

    # ATR Calculation
    exportable_df['ATR'] = exportable_df['High'].rolling(window=14).max() - exportable_df['Low'].rolling(window=14).min()

    # RSI Calculation
    delta = exportable_df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    exportable_df['RSI'] = 100 - (100 / (1 + rs))

    return exportable_df

# Function to calculate support and resistance
fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]

# Function to check if a value matches a Fibonacci level (within a tolerance)
def check_fibonacci_level(value):
    tolerance = 0.0001  # Define a small tolerance to account for rounding differences
    for level in fib_levels:
        if np.isclose(value, level, atol=tolerance):  # np.isclose checks if values are close to each other within a tolerance
            return True
    return False

def support_and_resistance():
    global exportable_df  # Use the global DataFrame
    
    # Calculate support and resistance levels
    exportable_df['Support'] = exportable_df['Low'].rolling(window=20).min()
    exportable_df['Resistance'] = exportable_df['High'].rolling(window=20).max()

    # Filter for strong levels by checking if Support or Resistance match Fibonacci levels
    exportable_df['Fib_Level_Support'] = exportable_df['Support'].apply(
        lambda x: check_fibonacci_level(x)
    )
    
    exportable_df['Fib_Level_Resistance'] = exportable_df['Resistance'].apply(
        lambda x: check_fibonacci_level(x)
    )
    
    # Label strong support and resistance based on Fibonacci matching
    exportable_df['Strong_Support'] = np.where(exportable_df['Fib_Level_Support'], exportable_df['Support'], np.nan)
    exportable_df['Strong_Resistance'] = np.where(exportable_df['Fib_Level_Resistance'], exportable_df['Resistance'], np.nan)
    
    # Only return rows where either strong support or resistance is present
    strong_levels_df = exportable_df[
        exportable_df['Fib_Level_Support'] | exportable_df['Fib_Level_Resistance']
    ]

    return strong_levels_df  # Return DataFrame with strong levels
# Function to plot data
def plot_combined_data():
    global exportable_df  # Use the global DataFrame

    plt.figure(figsize=(12, 12))

    # Subplot 1: Closing Price and Moving Averages
    plt.subplot(2, 1, 1)
    plt.plot(exportable_df['Date'], exportable_df['Close'], label='Close Price', color='blue')
    plt.plot(exportable_df['Date'], exportable_df['MA50'], label='50-Day MA', color='red')
    plt.plot(exportable_df['Date'], exportable_df['MA9'], label='9-Day MA', color='green')
    plt.title('Close Price and Moving Averages')
    plt.legend()
    plt.grid(True)

    # Subplot 2: Support, Resistance, Fibonacci Levels, and RSI
    plt.subplot(2, 1, 2)
    last_n_closes = exportable_df['Close'].tail(20)

    # Support and Resistance Levels
    support_level = last_n_closes.min()
    resistance_level = last_n_closes.max()

    plt.plot(exportable_df['Date'].tail(20), last_n_closes, label='Close Prices', marker='o', color='blue')

    # Plot support and resistance
    plt.axhline(support_level, color='green', linestyle='--', label=f'Support: {support_level:.2f}')
    plt.axhline(resistance_level, color='red', linestyle='--', label=f'Resistance: {resistance_level:.2f}')

    # Fibonacci Retracement Levels
    diff = resistance_level - support_level
    fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    fib_retracements = [support_level + (diff * level) for level in fib_levels]

    for i, fib_level in enumerate(fib_retracements):
        plt.axhline(fib_level, color='purple', linestyle=':', label=f'Fib {fib_levels[i] * 100:.1f}%: {fib_level:.2f}')

    # Plot Moving Averages
    plt.plot(exportable_df['Date'].tail(20), exportable_df['MA5'].tail(20), label='MA 5', color='orange')
    plt.plot(exportable_df['Date'].tail(20), exportable_df['MA9'].tail(20), label='MA 9', color='green')
    plt.plot(exportable_df['Date'].tail(20), exportable_df['MA50'].tail(20), label='MA 50', color='red')

    # RSI
    plt.plot(exportable_df['Date'], exportable_df['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')

    plt.title('Support, Resistance, Fibonacci Levels, Moving Averages, and RSI')
    plt.xlabel('Date')
    plt.ylabel('Price / RSI')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def trading_signal(amount_to_trade, instrument, url, headers):
    global exportable_df  # Use the global DataFrame

    # Ensure the necessary columns are present in the DataFrame
    required_columns = ['Close', 'MA5', 'MA9', 'MA50', 'ATR']
    if not all(col in exportable_df.columns for col in required_columns):
        raise ValueError("DataFrame must contain required columns: 'Close', 'MA5', 'MA9', 'MA50', 'ATR'")

    # Latest row (most recent data)
    latest_data = exportable_df.iloc[-1]

    # Fibonacci levels from support to resistance
    support_level = exportable_df['Close'].tail(20).min()
    resistance_level = exportable_df['Close'].tail(20).max()
    diff = resistance_level - support_level
    fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    fib_retracements = [support_level + (diff * level) for level in fib_levels]

    # ATR-based stop loss/take profit
    atr_multiplier = 1.5
    dynamic_stop_loss = latest_data['ATR'] * atr_multiplier
    dynamic_take_profit = latest_data['ATR'] * atr_multiplier * 2

    # Determine pip distance (10 pips = 0.0010 for 4 decimal places)
    pip_distance = 0.0010

    # Trading signal logic
    buy_condition = (
        (latest_data['MA5'] > latest_data['MA9']) and
        any(abs(latest_data['Close'] - fib_level) < 0.002 * latest_data['Close'] for fib_level in fib_retracements) and
        (latest_data['Close'] <= latest_data['Close'] + pip_distance)  # Within 10 pips above the closing price
    )

    sell_condition = (
        (latest_data['MA5'] < latest_data['MA9']) and
        any(abs(latest_data['Close'] - fib_level) < 0.002 * latest_data['Close'] for fib_level in fib_retracements) and
        (latest_data['Close'] >= latest_data['Close'] - pip_distance)  # Within 10 pips below the closing price
    )

    # Order details
    stop_loss_price = None
    take_profit_price = None
    order_type = 'MARKET_IF_TOUCHED'  # Default order type

    # Determine buy or sell signal
    if buy_condition:
        stop_loss_price = f"{latest_data['Close'] - dynamic_stop_loss:.5f}"
        take_profit_price = f"{latest_data['Close'] + dynamic_take_profit:.5f}"
        print(f"Buy signal generated for {instrument} at price {latest_data['Close']:.5f}")
        return "Buy", latest_data['Close'], order_type, stop_loss_price, take_profit_price

    elif sell_condition:
        stop_loss_price = f"{latest_data['Close'] + dynamic_stop_loss:.5f}"
        take_profit_price = f"{latest_data['Close'] - dynamic_take_profit:.5f}"
        print(f"Sell signal generated for {instrument} at price {latest_data['Close']:.5f}")
        return "Sell", latest_data['Close'], order_type, stop_loss_price, take_profit_price

    else:
        print(f"No trading signal for {instrument}. Hold.")
        return "Hold", latest_data['Close'], order_type  # Return order type with hold





        
# def trade(amount_to_trade, instrument, url, headers):
    
#     latest_data = exportable_df.iloc[-1]

    
#     strong_support_levels = exportable_df[exportable_df['Strong_Support'].notna()].sort_values(by='Support', ascending=True)
#     strong_resistance_levels = exportable_df[exportable_df['Strong_Resistance'].notna()].sort_values(by='Resistance', ascending=False)

#     next_strong_support = strong_support_levels['Support'].iloc[-1] if not strong_support_levels.empty else None
#     next_strong_resistance = strong_resistance_levels['Resistance'].iloc[0] if not strong_resistance_levels.empty else None
#     stop_loss_price = f"{next_strong_support:.5f}" if next_strong_support else f"{latest_data['Close'] - (0.005 * latest_data['Close']):.5f}"
#     take_profit_price = f"{next_strong_resistance:.5f}" if next_strong_resistance else f"{latest_data['Close'] + (0.0125 * latest_data['Close']):.5f}"

#     order_payload = {
#             "order": {
#                 "price": f"{latest_data['Close']:.5f}",  # Entry price
#                 "stopLossOnFill": {
#                     "timeInForce": "GTC",
#                     "price": stop_loss_price
#                 },
#                 "takeProfitOnFill": {
#                     "price": take_profit_price
#                 },
#                 "timeInForce": "GTC",
#                 "instrument": instrument,
#                 "units": f"{amount_to_trade}",  # Positive for buying
#                 "type": "LIMIT",  # Assuming it's a limit order
#                 "positionFill": "DEFAULT"
#             }
#         }

#         # Make the POST request to place the order
#     response = requests.post(url, headers=headers, json=order_payload)



