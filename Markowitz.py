import markowitzify
import os
import pandas as pd

def list_spy_holdings() -> pd.DataFrame:
    # Ref: https://stackoverflow.com/a/75845569/
    # Source: https://www.ssga.com/us/en/intermediary/etfs/funds/spdr-sp-500-etf-trust-spy
    # Note: One of the included holdings is CASH_USD.
    url = 'https://www.ssga.com/us/en/intermediary/etfs/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx'
    return pd.read_excel(url, engine='openpyxl', index_col='Ticker', skiprows=4).dropna()

def main():
    key = os.environ.get('API_Key')
    portfolio_object = markowitzify.portfolio(API_KEY = key)
    portfolio_object.build_portfolio(datareader = False, TKR_list = ['AAPL', 'MSFT', 'AMZN'], time_delta = 200)
    portfolio_object.markowitz()
    print(portfolio_object.optimal)

if __name__ == '__main__':
    main()
    