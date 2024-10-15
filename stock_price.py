import logging.config
import yfinance as yf
import pandas as pd
import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns

# os.walk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_stock_price(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.history(period="1y")
    
    if not stock_info.empty:
        closing_price = stock_info['Close'].iloc[0]
        return closing_price
    else:
        logging.info(f"Could not retrieve data for {stock_symbol}")
    
    
def get_stock_data(stock_symbol, period='1y'):
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(period=period)
    
    if not stock_data.empty:
        return stock_data
    else:
        logging.info(f"Could not retrieve data for {stock_symbol}")
        return None
    

def analyze_stock(stock_symbol):
    stock_data = get_stock_data(stock_symbol)
    
    if stock_data is not None:
        stock_data = add_moving_averages(stock_data)
        stock_data = add_bollinger_bands(stock_data)
        stock_data = calculate_rsi(stock_data)
        stock_data = generate_signals(stock_data)
    
        logging.info("\n=== Signals for Trading ===")
        logging.info(stock_data[['Close', 'SMA_20', 'SMA_50', 'RSI', 'Signals']].tail(10))
        stock_data['Percent Change'] = stock_data['Close'].pct_change() * 100 
        
        """ logging.info(f"\n=== {stock_symbol} Analysis ===")
        logging.info(f"Total Days: {len(stock_data)}")
        logging.info(f"Most recent closing price: ${stock_data['Close'].iloc[-1]:.2f}")
        logging.info(f"Highest price: ${stock_data['High'].max():.2f}")
        logging.info(f"Lowest price: ${stock_data['Low'].min():.2f}")
        logging.info(f"Average closing price: ${stock_data['Close'].mean():.2f}")
        logging.info(f"Biggest daily percent increase: {stock_data['Percent Change'].max():.2f}%")
        logging.info(f"Biggest daily percent drop: {stock_data['Percent Change'].min():.2f}%")
        
        logging.info("\nLast 5 days of stock data: ")
        logging.info(stock_data.tail()) """
        
        visualize_stock_data(stock_data, stock_symbol)
    else:
        logging.info(f"No data founnd for {stock_symbol}")
        
    
def analyze_multiple_stocks(stock_symbols):
    for symbol in stock_symbols:
        analyze_stock(symbol)
        
def visualize_stock_data(stock_data, stock_symbol):
    sns.set(style='whitegrid')
    plt.figure(figsize=(14, 7))

    plt.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='blue')
    plt.plot(stock_data.index, stock_data['SMA_20'], label='20-Day SMA', color='orange')
    plt.plot(stock_data.index, stock_data['SMA_50'], label='50-Day SMA', color='green')
    
    # Plot buy/sell signals
    buy_signals = stock_data[stock_data['Signal'] == 1]
    sell_signals = stock_data[stock_data['Signal'] == -1]
    
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)

    plt.title(f'{stock_symbol} Price Analysis with Trading Signals')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    
def add_moving_averages(stock_data, short_window=20, long_window=50):
    stock_data['SMA_20'] = stock_data['Close'].rolling(window=short_window).mean()
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=long_window).mean()
    return stock_data


def calculate_rsi(stock_data, window=14):
    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rollimg(window=window).mean()
    rs = gain / loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))
    return stock_data


def add_bollinger_bands(stock_data, window=20, num_std_dev=2):
    stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()
    stock_data['Upper Band'] = stock_data['SMA'] + (stock_data['Close'].rolling(window=window).std() * num_std_dev)
    stock_data['Lower Band'] = stock_data['SMA'] - (stock_data['Close'].rolling(window=window).std() * num_std_dev)


def generate_signals(stock_data):
    stock_data['Signal'] = 0
    stock_data.loc[(stock_data['SMA_20'] > stock_data['SMA_50']) & (stock_data['RSI'] < 30), 'Signal'] = 1
    stock_data.loc[(stock_data['SMA_20'] > stock_data['SMA_50']) & (stock_data['RSI'] < 70), 'Signal'] = -1
    return stock_data

  
stock_symbol = "AAPL"  
price = get_stock_price(stock_symbol)

if price:
    logging.info(f"The current price of {stock_symbol} is: ${price:.2f}")
else:
    logging.info(f"Price data for {stock_symbol} is unavailable.")
    
# analyze_stock(stock_symbol)
sale = get_stock_data(stock_symbol)
multiple_stocks = ["AAPL", "MSFT", "GOOG"]
analyze_multiple_stocks(multiple_stocks)


dir = 'Data Analysis/stockPrice'
os.makedirs(dir, exist_ok= True)
route = os.path.join(dir, 'stock.csv')
pd.DataFrame(sale).to_csv(route) 



















# yfinance is a librart used to download financial data fsrom Yahoo Finance
# The "ticker" object allows access market data for a given stock symbol

# "pandas(pd)" is a data manipulation and analysis library
# It is used here to handle the stock data which comes in the form of a DataFrame

# Functions
# get_stock_price(stock_market)

""" 
"stock_symbol" is equal to the "multiple_stocks" variable
"yf.Ticker(stock_symbol)" creates an object to fetch market data for the given symbol
"stock.history(period="1d")" retrieves historical data for the past day
"stock_info['Close].iloc[0]" extracts the most recent vlosing price from the returned data    
"""

# get_stock_data(stock_symbol, period='1y')

""" 
This function fetches hidtorical data for a stock over a specified period
Returns the data as a pandas DataFrame, or logging.infos a message if no data is available  
"""

# analyze_stock(stock_symbol)

""" 
Fetches stock data using "get_stock_data()" and performs basic analysis
logging.infos Key statistics
"""

# analyze_multiple_stocks(stock_symbols)

""" 
Takes a list of stock symbols and analyzes each using the "analyze_stock()" function
"""