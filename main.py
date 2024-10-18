
import logging
import os
import pandas as pd
from stock_analysis.stock_analyer import StockAnalyzer


# os.walk
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    stock_symbol = "AAPL" 
    analyzer = StockAnalyzer(stock_symbol)
    
    price = analyzer.get_stock_price()
    if price:
        logging.info(f"The current price of {stock_symbol} is: ${price:.2f}")
    else:
        logging.info(f"Price data for {stock_symbol} is unavailable.")
        
    analyzer.get_stock_data()
    analyzer.analyze_stock()


    if analyzer.stock_data is not None:
        dir = 'Data Analysis/stockPrice'
        os.makedirs(dir, exist_ok= True)
        route = os.path.join(dir, 'stock.csv')
        pd.DataFrame(analyzer.stock_data).to_csv(route) 
        logging.info(f"Stock data saved to {route}")
    else:
        logging.info("No stock data avaible to save")

    multiple_stocks = ["AAPL", "MSFT", "GOOG"]
    analyzer.analyze_multiple_stocks(multiple_stocks)
    
if __name__ == "__main__":
    main()

    

 



















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