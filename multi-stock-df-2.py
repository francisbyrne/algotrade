"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt

benchmark_symbol = '^AXJO'

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if benchmark_symbol not in symbols:  # add benchmark for reference, if absent
        symbols.insert(0, benchmark_symbol)

    for symbol in symbols:
        path = symbol_to_path(symbol)

        # Read data in from csv file
        dfStock = pd.read_csv(path,
                    index_col = "Date",
                    parse_dates = True,
                    usecols = ['Date', 'Adj Close'],
                    na_values = ['nan'])

        # Rename adj close column to symbol name
        dfStock = dfStock.rename(columns={'Adj Close': symbol})

        # Round to two dec. places
        dfStock = dfStock.round(2)

        # Join with main dataframe
        df = df.join(dfStock)

        # Drop any dates benchmark didn't trade on
        if symbol == benchmark_symbol:
            df = df.dropna(subset=[benchmark_symbol])

    return df

def plot_data(df, title="Stock prices"):
    ax = df.plot(title=title, fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    slicedDf = df.ix[start_index:end_index, columns]
    slicedDf.plot()
    plt.show()

def normalize_data(df):
    return df / df.ix[0,:]

def compute_daily_returns(df):
    # Match rows and columns of original dataframe
    daily_returns = df.copy()

    # Compute daily returns for row 1 onwards
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1

    # Initial row is uncalculatable, so set it to 0
    daily_returns.ix[0, :] = 0

    return daily_returns

def compute_rolling_mean(df, window=20):
    return df.rolling(window).mean()

def test_run():
    # Define a date range
    dates = pd.date_range('2016-07-22', '2016-11-22')

    # Choose stock symbols to read
    symbols = ['CTD.AX']

    # Get stock data
    df = get_data(symbols, dates)

    # df = normalize_data(df)

    # Print subset of data range
    # print(df.ix['2010-03-01':'2010-03-31', ['SPY', 'IBM', 'GOOG']])
    # plot_data(df)

    # print('Mean:\n', df.mean())
    # print('Median:\n', df.median())
    # print('Mode:\n', df.mode())
    # print('Std:\n', df.std())

    # rolling_mean = df.rolling(20).mean()
    # plot_data(rolling_mean)

    daily_returns = compute_daily_returns(df)
    rolling_daily_return = compute_rolling_mean(daily_returns)
    plot_data(rolling_daily_return)



if __name__ == "__main__":
    test_run()
