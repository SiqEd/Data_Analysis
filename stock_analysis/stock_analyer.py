import logging
import yfinance as yf
from stock_analysis.indicators import add_bollinger_bands, add_moving_averages, calculate_rsi
from stock_analysis.signals import generate_signals
from stock_analysis.visualization import visualize_stock_data

class StockAnalyzer:
    def __init__(self, stock_symbol, period='1y'):
        self.stock_symbol = stock_symbol
        self.period = period
        self.stock_data = None
        
    def get_stock_data(self):
        stock = yf.Ticker(self.stock_symbol)
        stock_data = stock.history(period=self.period)
        
        if not stock_data.empty:
            self.stock_data = stock_data
            return stock_data
        else:
            logging.info(f"Could not retrieve data for {self.stock_symbol}")
            return None
    
    
    def get_stock_price(self):
        stock = yf.Ticker(self.stock_symbol)
        stock_info = stock.history(period="1y")
    
        if not stock_info.empty:
            closing_price = stock_info['Close'].iloc[-1]
            return closing_price
        else:
            logging.info(f"Could not retrieve data for {self.stock_symbol}")
        
    
    def analyze_stock(self):
        if self.stock_data is None:
            self.get_stock_data()
        
        if self.stock_data is not None:
            stock_data = self.stock_data
            stock_data = add_moving_averages(stock_data)
            stock_data = add_bollinger_bands(stock_data)
            stock_data = calculate_rsi(stock_data)
            stock_data = generate_signals(stock_data)
        
            logging.info("\n=== Signals for Trading ===")
            logging.info(stock_data[['Close', 'SMA_20', 'SMA_50', 'RSI', 'Signal']].tail(10))
            stock_data['Percent Change'] = stock_data['Close'].pct_change() * 100 
            
            logging.info(f"\n=== {self.stock_symbol} Analysis ===")
            logging.info(f"Total Days: {len(stock_data)}")
            logging.info(f"Most recent closing price: ${stock_data['Close'].iloc[-1]:.2f}")
            logging.info(f"Highest price: ${stock_data['High'].max():.2f}")
            logging.info(f"Lowest price: ${stock_data['Low'].min():.2f}")
            logging.info(f"Average closing price: ${stock_data['Close'].mean():.2f}")
            logging.info(f"Biggest daily percent increase: {stock_data['Percent Change'].max():.2f}%")
            logging.info(f"Biggest daily percent drop: {stock_data['Percent Change'].min():.2f}%")
            
            logging.info("\nLast 5 days of stock data: ")
            logging.info(stock_data.tail())
            
            visualize_stock_data(stock_data, self.stock_symbol)
        else:
            logging.info(f"No data founnd for {self.stock_symbol}")
            
    def analyze_multiple_stocks(self, stock_symbols):
        for symbol in stock_symbols:
            logging.info(f"Analyzing {symbol}...")
            self.stock_symbol = symbol
            self.get_stock_data()
            self.analyze_stock()