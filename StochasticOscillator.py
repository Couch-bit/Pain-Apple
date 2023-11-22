from plotly.subplots import make_subplots
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf

def main():
    df = yf.Ticker('aapl')
    df = df.history(period='6mo')[['Open', 'High', 'Low', 'Close']]
    df = pd.concat([df, df.ta.stoch(high='high', low='low', k=14, d=3)], axis = 1)
    df.columns = [x.lower() for x in df.columns]
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
        # Font Families
        font_family='Times New Roman',
        font_color='black',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )
    fig.update_layout(layout)
    fig.show()


if __name__ == '__main__':
    main()
    
