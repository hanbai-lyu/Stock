import pandas as pd

if __name__ == "__main__":
    data_stock = pd.read_csv('Raw data/Raw data summary copy.csv').set_index('Date')
    data_shares = {}
    data_shares_raw = pd.read_csv('Raw data/Share data.csv').set_index('Company')
    # data_stock contains adjusted close price for long and raw close price for short

    # Write the number of shares in a dictionary; positive for long, negative for short
    for index, row in data_shares_raw.iterrows():
        if row['Long']:
            data_shares[index] = row['Share']
        else:
            data_shares[index] = -row['Share']

    # Calculate daily difference of adjusted close price (long) or close price (short)
    data_stock = data_stock.join(data_stock.diff(), rsuffix='_diff')

    data_stock['tot_cap'] = 0
    data_stock['tot_ret'] = 0

    # The total capital is the sum of t-1 (adjusted) close * shares
    # For long position, the return is the t-(t-1) difference of adjusted close * shares
    # For short position, the return is the (t-1)-t difference of raw close * shares
    for company in data_shares:
        data_stock['tot_cap'] += data_stock[company] * abs(data_shares[company])
        data_stock['tot_ret'] += data_stock[company + '_diff'] * data_shares[company]
    data_stock['tot_ret'] /= data_stock['tot_cap'].shift()
    data_stock.tot_ret.dropna().to_csv('Total return.csv')
