import markowitzify
import os

def main():
    key = os.environ.get('API_Key')
    portfolio_object = markowitzify.portfolio(API_KEY=key)
    portfolio_object.build_portfolio(datareader=False, TKR_list=['AAPL', 'MSFT', 'AMZN'], time_delta=200)
    portfolio_object.markowitz()
    print(portfolio_object.optimal)

if __name__ == '__main__':
    main()
    