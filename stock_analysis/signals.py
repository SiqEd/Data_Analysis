

def generate_signals(stock_data):
    stock_data['Signal'] = 0
    stock_data.loc[(stock_data['SMA_20'] > stock_data['SMA_50']) & (stock_data['RSI'] < 30), 'Signal'] = 1
    stock_data.loc[(stock_data['SMA_20'] > stock_data['SMA_50']) & (stock_data['RSI'] > 70), 'Signal'] = -1
    return stock_data