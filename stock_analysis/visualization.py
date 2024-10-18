import matplotlib.pyplot as plt
import seaborn as sns

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