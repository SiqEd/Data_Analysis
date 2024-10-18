import pandas as pd


def add_moving_averages(stock_data, short_window=20, long_window=50):
    stock_data['SMA_20'] = stock_data['Close'].rolling(window=short_window).mean()
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=long_window).mean()
    return stock_data

def calculate_rsi(stock_data, window=14):
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    return stock_data

def add_bollinger_bands(stock_data, window=20, num_std_dev=2):
    stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()
    stock_data['Upper Band'] = stock_data['SMA'] + (stock_data['Close'].rolling(window=window).std() * num_std_dev)
    stock_data['Lower Band'] = stock_data['SMA'] - (stock_data['Close'].rolling(window=window).std() * num_std_dev)
    return stock_data