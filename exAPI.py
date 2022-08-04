#0PB7QVJ9Z7XQB4T8
import pandas as pd
import requests
import io
import csv
import itertools
import plotly.graph_objects as go

def API_current_price(ticker):
    url='https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+ticker+'&apikey=0PB7QVJ9Z7XQB4T8'
    var=requests.get(url)
    var=var.json()
    var=float(var['Global Quote']['05. price'])
    return var

def API_intraday(ticker,interval):
    """ supported intervals: 1min, 5min, 15min, 30min, 60min"""
    url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval='+str(interval)+'min&apikey=0PB7QVJ9Z7XQB4T8&datatype=csv'
    var=requests.get(url)
    df = pd.read_csv(io.StringIO(var.text), sep=',', quoting=csv.QUOTE_ALL)
    return df

def API_daily(ticker):
    url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=0PB7QVJ9Z7XQB4T8&datatype=csv'
    var=requests.get(url)
    df = pd.read_csv(io.StringIO(var.text), sep=',', quoting=csv.QUOTE_ALL)
    return df

def API_get_tickers():
    url='https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=0PB7QVJ9Z7XQB4T8'
    var=requests.get(url)
    df = pd.read_csv(io.StringIO(var.text), sep=',', quoting=csv.QUOTE_ALL)
    df = df[(df['exchange'] == 'NASDAQ')]
    df = df[(df['assetType'] == 'Stock')]
    df = df.drop(columns=['exchange', 'assetType', 'ipoDate', 'delistingDate','status'])
    return df

def API_search_ticker(tickers,text):
    df=tickers
    df["Indexes"] = df["name"].str.contains(text, case=False)
    df = df[(df['Indexes'] == True)]
    df = df.drop(columns=['Indexes'])
    # with pd.option_context(
    #         'display.width', None,
    #         'display.max_columns', None,
    #         'display.max_rows', None,
    #         'display.max_colwidth', -1,
    #         'display.colheader_justify', 'left'):
    #     print(df)
    return df

def API_get_info(ticker):
    url='https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ticker+'&apikey=0PB7QVJ9Z7XQB4T8&datatype=csv'
    var=requests.get(url)
    var=var.json()
    var=dict(itertools.islice(var.items(), 4))
    return var

def API_get_ticker_graph(ticker_dict,ticker):
    CandleGraph= go.Figure(data=[go.Candlestick(x=ticker_dict[ticker]['timestamp'],
                                  open=ticker_dict[ticker]['open'],
                                  high=ticker_dict[ticker]['high'],
                                  low=ticker_dict[ticker]['low'],
                                  close=ticker_dict[ticker]['close'],
                                 )])
    CandleGraph.update_layout(xaxis_rangeslider_visible=False)
    CandleGraph.update_layout(title={'text': ticker, 'x': 0.5})
    #CandleGraph.show()
    return CandleGraph



# API_get_info('MSFT')
# ticker_dict={}
# ticker='MSFT'
# ticker_dict.update ({ticker:API_intraday(ticker,60)})
# API_get_ticker_graph(ticker_dict,ticker)
# print(ticker_dict)

# fig = go.Figure(data=go.Scatter(x=ticker_dict[ticker]['timestamp'],y=ticker_dict[ticker]['close'], mode='lines'))
# fig.show()

# df=API_daily('MSFT')
# df.count()
# print(df['timestamp'].count())
#tickers = get_tickers()
#API_search_ticker(tickers,'microsoft')

#help(API_intraday)