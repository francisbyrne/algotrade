import pandas as pd

def test_run():
    # Create an empty dataframe with date range
    start_date = '2016-10-20'
    end_date = '2016-10-26'
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index = dates)

    symbols = ['SPY', 'AAPL', 'IBM']

    for symbol in symbols:
        # Read stock data into temporary dataframe
        dfStock = pd.read_csv("data/{}.csv".format(symbol),
                        index_col = "Date",
                        parse_dates = True,
                        usecols = ['Date', 'Adj Close'],
                        na_values = ['nan'])

        # Round to two dec places
        dfStock = dfStock.round(2)

        dfStock = dfStock.rename(columns={'Adj Close': symbol})

        # Join with main dataframe
        df1 = df1.join(dfStock, how='inner')

    print(df1)

if __name__ == "__main__":
    test_run()
