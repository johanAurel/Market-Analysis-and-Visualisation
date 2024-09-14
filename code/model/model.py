import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


def fetch_data(url):
    # Replace with your API URL
    response = requests.get(url)
    data = response.json()  # Assuming the data is in JSON format
    df= pd.DataFrame(data)
    return df

def indicator(df):
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA9'] = df['Close'].rolling(window=9).mean()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def support_and_resistance(df):
    # Assume df is your DataFrame with columns 'High', 'Low', 'Close' and 'Date'
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
