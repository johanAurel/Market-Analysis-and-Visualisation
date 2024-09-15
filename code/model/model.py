import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

def indicator(df):
    # Ensure 'Close', 'Price', and 'Volume' columns are present
    if 'Close' not in df.columns or 'Price' not in df.columns or 'Volume' not in df.columns:
        raise ValueError("DataFrame must contain 'Close', 'Price', and 'Volume' columns")

    # Calculate Moving Averages
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA9'] = df['Close'].rolling(window=9).mean()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # VWAP Calculation
    df['Cumulative Volume'] = df['Volume'].cumsum()
    df['Cumulative Price-Volume'] = (df['Price'] * df['Volume']).cumsum()
    df['VWAP'] = df['Cumulative Price-Volume'] / df['Cumulative Volume']
    
    return df

def support_and_resistance(df):
    # Ensure 'High' and 'Low' columns are present
    if 'High' not in df.columns or 'Low' not in df.columns:
        raise ValueError("DataFrame must contain 'High' and 'Low' columns")

    # Calculate support and resistance
    df['Support'] = df['Low'].rolling(20).min()
    df['Resistance'] = df['High'].rolling(20).max()
    
    return df

def plot_data(df):
    plt.figure(figsize=(12, 6))
    
    # Plot Closing Price and Moving Averages
    plt.subplot(2, 1, 1)
    plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')
    plt.plot(df['Date'], df['MA50'], label='50-Day MA', color='red')
    plt.plot(df['Date'], df['MA9'], label='9-Day MA', color='green')
    plt.plot(df['Date'], df['VWAP'], label='VWAP', color='orange')
    plt.title('Close Price and Moving Averages')
    plt.legend()
    plt.grid(True)

    # Plot RSI
    plt.subplot(2, 1, 2)
    plt.plot(df['Date'], df['RSI'], label='RSI', color='purple')
    plt.title('Relative Strength Index (RSI)')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def trading_signal(df, amount_to_trade):
    
    # Ensure the necessary columns are present
    required_columns = ['Close', 'MA5', 'MA9', 'MA50', 'VWAP', 'Support', 'Resistance', 'RSI']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain required columns: 'Close', 'MA5', 'MA9', 'MA50', 'VWAP', 'Support', 'Resistance', 'RSI'")
    
    # Latest row (most recent data)
    latest_data = df.iloc[-1]
    
    # Trading Conditions
    buy_condition = (
        (latest_data['MA5'] > latest_data['MA9']) and
        (latest_data['MA9'] > latest_data['MA50']) and
        (latest_data['Close'] > latest_data['VWAP']) and
        (latest_data['Close'] > latest_data['Support']) and
        (latest_data['Close'] < latest_data['Resistance']) and
        (latest_data['RSI'] < 30)
    )
    
    sell_condition = (
        (latest_data['MA5'] < latest_data['MA9']) and
        (latest_data['MA9'] < latest_data['MA50']) and
        (latest_data['Close'] < latest_data['VWAP']) and
        (latest_data['Close'] > latest_data['Support']) and
        (latest_data['Close'] < latest_data['Resistance']) and
        (latest_data['RSI'] > 70)
    )
    
    if buy_condition:
        return f"Buy {amount_to_trade} units"
    elif sell_condition:
        return f"Sell {amount_to_trade} units"
    else:
        return "Hold"


