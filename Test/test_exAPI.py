from exAPI import *

def test_API_current_price():
    assert API_current_price('IBM') > 0

def test_api_intraday():
    df=API_intraday('IBM',5)
    assert df['timestamp'].count() == 100

def test_api_daily():
    df=API_daily('IBM')
    assert df['timestamp'].count() == 100

def test_API_get_tickers():
    df=API_get_tickers()
    assert df['symbol'].count()>1

def test_API_search_ticker():
    tickers = API_get_tickers()
    df=API_search_ticker(tickers,'microsoft')
    assert df['symbol'].count()>0

def test_API_get_info():
    dict=API_get_info('MSFT')
    assert len(dict) == 4

def test_API_get_ticker_graph():
    ticker_dict={}
    ticker='MSFT'
    ticker_dict.update ({ticker:API_intraday(ticker,60)})
    candlegraph = API_get_ticker_graph(ticker_dict,ticker)
    assert candlegraph

