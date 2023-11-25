import markowitzify
import os
from plotly.subplots import make_subplots
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf

def stoch(ticker : str):

    low = 20
    high = 80

    try:
        df = yf.Ticker(ticker)
        df = df.history(period='6mo')[['Open', 'High', 'Low', 'Close']]
        df = pd.concat([df, df.ta.stoch(high='high', low='low', k=14, d=3)], axis = 1)
        df.columns = [x.lower() for x in df.columns]
    except:
        print('No such stock')
        return

    fig = make_subplots(rows=2, cols=1)
    
    fig.append_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='orange',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1
    )
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['open'],
            line=dict(color='orange', width=1),
            name='open',
        ), row=1, col=1
    )

    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['stochk_14_3_3'],
            line=dict(color='orange', width=2),
            name='fast',
        ), row=2, col=1
    )
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['stochd_14_3_3'],
            line=dict(color='black', width=2),
            name='slow'
        ), row=2, col=1
    )

    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    fig.add_hline(y=0, col=1, row=2, line_color="black", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="black", line_width=2)
    fig.add_hline(y=20, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')

    layout = go.Layout(
        plot_bgcolor='#EEE',
        font_family='Times New Roman',
        font_color='black',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        title=ticker,
        title_font_size=40
    )

    fig.update_layout(layout)
    fig.show()

    slow = df.tail(1)['stochd_14_3_3'][0]
    fast = df.tail(1)['stochk_14_3_3'][0]

    if slow > fast and fast > high:
        print(f"{ticker} - Sell")
    elif fast > slow and fast < low:
        print(f"{ticker} - Buy")

def build_portfolio(tickers_list: list) -> markowitzify.portfolio:
    key = os.environ.get('API_Key')
    portfolio_object = markowitzify.portfolio(API_KEY=key)
    portfolio_object.build_portfolio(datareader=False, TKR_list=tickers_list, time_delta=200)
    portfolio_object.markowitz()
    return portfolio_object

def main():
    try:
        portfolio = pd.read_csv("weights.csv", index_col=0)
        print("Portfolio file found, do you wish to load it? (yes, no):")
        response = input()
        while response not in ["yes", "no"]:
            print("Invalid input, try again:")
            response = input()
    except:
        print("No Portfolio file found")
        response = "no"
    
    if response == "no":
        try:
            print("Please input the tickers of potential investments:")
            tickers = input().strip().split()
            portfolio = build_portfolio(tickers).optimal.T
            portfolio.columns = ['weights']
            portfolio.to_csv("weights.csv")
            print(portfolio)
        except:
            print("Invalid stocks, closing...")
            return
    else:
        print(portfolio)
    
    for i in portfolio.index:
        stoch(i)

if __name__ == '__main__':
    main()
    