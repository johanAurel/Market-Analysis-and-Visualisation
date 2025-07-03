import pandas as pd
import numpy as np
import requests
import time

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


exportable_df = pd.DataFrame()  # Your price DataFrame must be populated externally

def calculate_atr(df, period=14):
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df['ATR'].iloc[-1]

def trade(amount_to_trade, instrument, url, headers):
    # Replace this with your real trade execution logic using POST to OANDA
    return {
        "orderFillTransaction": {
            "tradeOpened": {"tradeID": "simulated_trade_id_123"}
        }
    }

def close_trade(trade_id, url, headers):
    close_url = f"{url}/v3/accounts/{headers['accountID']}/trades/{trade_id}/close"
    response = requests.put(close_url, headers=headers)
    return response.status_code == 200, response.text

def orb_strategy(amount_to_trade, instrument, url, headers, exportable_df, existing_position=None):
    if exportable_df.empty or len(exportable_df) < 30:
        return None

    df = exportable_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = df['Date'].dt.time
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    # === Configuration (matches Pine Script) ===
    open_range_start_hour = 8
    open_range_start_minute = 30
    open_range_duration_minutes = 15
    trade_end_hour = 16
    trade_end_minute = 0
    min_breakout_pct = 0.001
    atr_length = 14
    atr_multiplier = 1.0
    pip = 0.0001

    # === Prepare Today's Data ===
    today = df['Date'].iloc[-1].date()
    df_today = df[df['Date'].dt.date == today]
    if df_today.empty:
        return None

    # === Time Boundaries ===
    range_start = pd.Timestamp.combine(today, pd.Timestamp(f"{open_range_start_hour}:{open_range_start_minute}").time())
    range_end = range_start + pd.Timedelta(minutes=open_range_duration_minutes)
    trade_start = range_end
    trade_end = pd.Timestamp.combine(today, pd.Timestamp(f"{trade_end_hour}:{trade_end_minute}").time())

    # === Define Open Range ===
    range_data = df_today[(df_today['Date'] >= range_start) & (df_today['Date'] < range_end)]
    if range_data.empty:
        return None

    open_range_high = range_data['High'].max()
    open_range_low = range_data['Low'].min()

    # === Current Time and Validity Window ===
    latest = df_today.iloc[-1]
    prev = df_today.iloc[-2]
    now = latest['Date']

    in_trade_time = (now >= trade_start) and (now <= trade_end)

    if not in_trade_time:
        return None

    # === ATR Calculation ===
    df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=atr_length).mean()
    atr_value = df['ATR'].iloc[-1]

    # === Confirmed Breakout Logic ===
    breakout_long = (
        (prev['Close'] <= open_range_high * (1 + min_breakout_pct)) and
        (latest['Close'] > open_range_high * (1 + min_breakout_pct) + pip)
    )

    breakout_short = (
        (prev['Close'] >= open_range_low * (1 - min_breakout_pct)) and
        (latest['Close'] < open_range_low * (1 - min_breakout_pct) - pip)
    )

    # === Prevent Duplicate Positions ===
    if existing_position == 'long' and breakout_long:
        return None
    if existing_position == 'short' and breakout_short:
        return None

    # === Entry and Stop Calculation ===
    stop_offset = atr_value * atr_multiplier

    if breakout_long:
        t = trade(amount_to_trade, instrument, url, headers)
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
        t = trade('-' + amount_to_trade, instrument, url, headers)
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

def vwap_strategy(amount_to_trade, instrument, url, headers):
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
        t = trade(amount_to_trade, instrument, url, headers)
        return {
            'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
            'direction': 'long',
            'entry_price': latest['Close'],
            'bars_held': 0,
            'entry_time': latest['Date'],
            'trade_log': []
        }

    elif prev['Close'] > prev['UpperBand'] and latest['Close'] < latest['UpperBand']:
        t = trade('-' + amount_to_trade, instrument, url, headers)
        return {
            'trade_id': t['orderFillTransaction']['tradeOpened']['tradeID'],
            'direction': 'short',
            'entry_price': latest['Close'],
            'bars_held': 0,
            'entry_time': latest['Date'],
            'trade_log': []
        }

    return None

def manage_open_trade(current_trade, instrument, url, headers):
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

    stop_hit = False
    if direction == 'long':
        stop_price = entry_price - (atr * 1.0)
        stop_hit = close_price <= stop_price
    else:
        stop_price = entry_price + (atr * 1.0)
        stop_hit = close_price >= stop_price

    # Average bar check (optional, here simplified)
    max_bars = 15  # You can make this dynamic based on `current_trade['trade_log']`

    if stop_hit or bars_held > max_bars:
        success, msg = close_trade(current_trade['trade_id'], url, headers)
        if success:
            pnl = (close_price - entry_price) if direction == 'long' else (entry_price - close_price)
            current_trade['trade_log'].append({'bars': bars_held, 'result': pnl})
            print(f"Trade {current_trade['trade_id']} closed after {bars_held} bars.")
            return None
        else:
            print(f"Failed to close trade: {msg}")
            return current_trade

    return current_trade

def run_strategies(amount_to_trade, instrument, url, headers, current_trade=None):
    if current_trade is None:
        trade_result = vwap_strategy(amount_to_trade, instrument, url, headers)
        if trade_result is None:
            trade_result = orb_strategy(amount_to_trade, instrument, url, headers)
        return trade_result
    else:
        return manage_open_trade(current_trade, instrument, url, headers)

# Usage example:
# current_trade = None
# while True:
#     # fetch candles and create dataframe
#     create_dataframe(your_candles_data)
#     current_trade = run_strategies(100, 'EUR_USD', your_order_url, your_headers, current_trade)
#     time.sleep(60)

