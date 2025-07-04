import pandas as pd
import numpy as np
import requests
import questionary
from model.variables import ORDERS
import time  # Allowed since your imports imply stdlib usage

# Global DataFrame to hold candles
exportable_df = pd.DataFrame()

def create_dataframe(candlesticks):
    global exportable_df
    data = {
        'Date': [candle['time'] for candle in candlesticks],
        'Open': [float(candle['mid']['o']) for candle in candlesticks],
        'High': [float(candle['mid']['h']) for candle in candlesticks],
        'Low': [float(candle['mid']['l']) for candle in candlesticks],
        'Close': [float(candle['mid']['c']) for candle in candlesticks],
        'Volume': [candle['volume'] for candle in candlesticks]
    }
    exportable_df = pd.DataFrame(data)
    exportable_df['Date'] = pd.to_datetime(exportable_df['Date'])
    exportable_df['Price'] = exportable_df['Close']
    return exportable_df

def trade(units, ticker, headers):
    body = {
        "order": {
            "units": str(units),
            "ticker": ticker,
            "timeInForce": "GTC",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    
    response = requests.post(
        ORDERS['POST']['CREATE_ORDER_URL'],
        headers=headers,
        json=body
    )

    if response.status_code == 201:
        return response.json()
    else:
        print(f"Trade failed: {response.text}")
        return None

def reverse_trade(current_trade, amount_to_trade, ticker, headers):
    if current_trade['direction'] == 'long':
        return trade(-int(amount_to_trade), ticker, headers)
    elif current_trade['direction'] == 'short':
        return trade(int(amount_to_trade), ticker,headers)
    return None

def orb_strategy(amount_to_trade, ticker, headers, exportable_df, existing_position=None):
    if exportable_df.empty or len(exportable_df) < 30:
        return None

    df = exportable_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = df['Date'].dt.time
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    open_range_start_hour = 8
    open_range_start_minute = 30
    open_range_duration_minutes = 15
    trade_end_hour = 16
    trade_end_minute = 0
    min_breakout_pct = 0.001
    atr_length = 14
    atr_multiplier = 1.0
    pip = 0.0001

    today = df['Date'].iloc[-1].date()
    df_today = df[df['Date'].dt.date == today]
    if df_today.empty:
        return None

    range_start = pd.Timestamp.combine(today, pd.Timestamp(f"{open_range_start_hour}:{open_range_start_minute}").time())
    range_end = range_start + pd.Timedelta(minutes=open_range_duration_minutes)
    trade_start = range_end
    trade_end = pd.Timestamp.combine(today, pd.Timestamp(f"{trade_end_hour}:{trade_end_minute}").time())

    range_data = df_today[(df_today['Date'] >= range_start) & (df_today['Date'] < range_end)]
    if range_data.empty:
        return None

    open_range_high = range_data['High'].max()
    open_range_low = range_data['Low'].min()

    latest = df_today.iloc[-1]
    prev = df_today.iloc[-2]
    now = latest['Date']

    in_trade_time = (now >= trade_start) and (now <= trade_end)
    if not in_trade_time:
        return None

    df['TR'] = np.maximum(df['High'] - df['Low'],
                          np.maximum(abs(df['High'] - df['Close'].shift(1)),
                                     abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=atr_length).mean()
    atr_value = df['ATR'].iloc[-1]

    breakout_long = (
        (prev['Close'] <= open_range_high * (1 + min_breakout_pct)) and
        (latest['Close'] > open_range_high * (1 + min_breakout_pct) + pip)
    )
    breakout_short = (
        (prev['Close'] >= open_range_low * (1 - min_breakout_pct)) and
        (latest['Close'] < open_range_low * (1 - min_breakout_pct) - pip)
    )

    stop_offset = atr_value * atr_multiplier

    if existing_position == 'long' and breakout_long:
        return None
    if existing_position == 'short' and breakout_short:
        return None

    if breakout_long:
        t = trade(amount_to_trade, ticker, headers)
        if t:
            return {
                'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
                'direction': 'long',
                'entry_price': latest['Close'],
                'entry_time': latest['Date'],
                'stop_loss': latest['Close'] - stop_offset,
                'trail_offset': stop_offset,
                'bars_held': 0,
                'trade_log': []
            }

    elif breakout_short:
        t = trade('-' + str(amount_to_trade), ticker, headers)
        if t:
            return {
                'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
                'direction': 'short',
                'entry_price': latest['Close'],
                'entry_time': latest['Date'],
                'stop_loss': latest['Close'] + stop_offset,
                'trail_offset': stop_offset,
                'bars_held': 0,
                'trade_log': []
            }

    return None

def vwap_strategy(amount_to_trade, ticker, headers, exportable_df):
    if exportable_df.empty or len(exportable_df) < 21:
        return None

    df = exportable_df.copy()
    vwap = (df['High'] + df['Low'] + df['Close']) / 3
    std = (df['Close'] - vwap).rolling(20).std()
    multiplier = 2.0

    df['VWAP'] = vwap
    df['UpperBand'] = vwap + multiplier * std
    df['LowerBand'] = vwap - multiplier * std

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    if prev['Close'] < prev['LowerBand'] and latest['Close'] > latest['LowerBand']:
        t = trade(amount_to_trade, ticker, headers)
        if t:
            return {
                'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
                'direction': 'long',
                'entry_price': latest['Close'],
                'bars_held': 0,
                'entry_time': latest['Date'],
                'trade_log': []
            }

    elif prev['Close'] > prev['UpperBand'] and latest['Close'] < latest['UpperBand']:
        t = trade('-' + str(amount_to_trade), ticker, headers)
        if t:
            return {
                'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
                'direction': 'short',
                'entry_price': latest['Close'],
                'bars_held': 0,
                'entry_time': latest['Date'],
                'trade_log': []
            }

    return None

def calculate_atr(df, length=14):
    df['TR'] = np.maximum(df['High'] - df['Low'],
                          np.maximum(abs(df['High'] - df['Close'].shift(1)),
                                     abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=length).mean()
    return df['ATR'].iloc[-1]

def manage_open_trade(current_trade, amount_to_trade, ticker, headers, exportable_df):
    if exportable_df.empty or current_trade is None:
        return None

    df = exportable_df.copy()
    latest = df.iloc[-1]
    close_price = latest['Close']

    current_trade['bars_held'] += 1
    atr = calculate_atr(df)
    direction = current_trade['direction']
    entry_price = current_trade['entry_price']
    bars_held = current_trade['bars_held']

    stop_hit = (close_price <= entry_price - atr) if direction == 'long' else (close_price >= entry_price + atr)
    max_bars = 15

    if stop_hit or bars_held > max_bars:
        reversed_trade = reverse_trade(current_trade, amount_to_trade, ticker, headers)
        if reversed_trade:
            pnl = (close_price - entry_price) if direction == 'long' else (entry_price - close_price)
            current_trade['trade_log'].append({'bars': bars_held, 'result': pnl})
            print(f"Reversed trade at bar {bars_held}")
            return None
        else:
            print(f"Failed to reverse trade")
            return current_trade

    return current_trade

def trade_single_instrument_continuous(amount_to_trade, ticker, headers, strategy_name):
    """
    Continuously trade one ticker with chosen strategy: 'orb' or 'vwap'
    """
    current_position = None
    strategy_name = strategy_name.lower()  # normalize to lowercase

    while True:
        # exportable_df must be updated externally with fresh candle data

        if strategy_name == 'orb':
            signal = orb_strategy(amount_to_trade, ticker, headers, exportable_df,
                                 existing_position=current_position['direction'] if current_position else None)
        elif strategy_name == 'vwap':
            signal = vwap_strategy(amount_to_trade, ticker, headers, exportable_df)
        else:
            print(f"Unknown strategy: {strategy_name.upper()}")
            break  # or return, to exit loop on unknown strategy

        if signal:
            current_position = signal
            print(f"New position opened: {current_position['direction']} at {current_position['entry_price']}")
        elif current_position:
            updated_position = manage_open_trade(current_position, amount_to_trade, ticker, headers, exportable_df)
            if updated_position is None:
                current_position = None
                print("Position closed")
            else:
                current_position = updated_position

        time.sleep(10)


def trade_all_instruments_continuous(amount_to_trade, tickers, headers, strategy_name):
    """
    Continuously trade multiple tickers with chosen strategy: 'orb' or 'vwap'
    """
    current_positions = {ticker: None for ticker in tickers}
    strategy_name = strategy_name.lower()  # normalize to lowercase

    while True:
        if strategy_name == 'orb':
            for ticker in tickers:
                signal = orb_strategy(amount_to_trade, ticker, headers, exportable_df,
                                     existing_position=current_positions[ticker]['direction'] if current_positions[ticker] else None)
                if signal:
                    current_positions[ticker] = signal
                    print(f"{ticker}: New position opened: {signal['direction']} at {signal['entry_price']}")
                elif current_positions[ticker]:
                    updated_position = manage_open_trade(current_positions[ticker], amount_to_trade, ticker, headers, exportable_df)
                    if updated_position is None:
                        current_positions[ticker] = None
                        print(f"{ticker}: Position closed")
                    else:
                        current_positions[ticker] = updated_position

        elif strategy_name == 'vwap':
            for ticker in tickers:  # fixed typo: tickers not ticker
                signal = vwap_strategy(amount_to_trade, ticker, headers, exportable_df)
                if signal:
                    current_positions[ticker] = signal
                    print(f"{ticker}: New position opened: {signal['direction']} at {signal['entry_price']}")
                elif current_positions[ticker]:
                    updated_position = manage_open_trade(current_positions[ticker], amount_to_trade, ticker, headers, exportable_df)
                    if updated_position is None:
                        current_positions[ticker] = None
                        print(f"{ticker}: Position closed")
                    else:
                        current_positions[ticker] = updated_position

        else:
            print(f"Unknown strategy: {strategy_name.upper()}")
            return  # exit on unknown strategy

        time.sleep(10)
