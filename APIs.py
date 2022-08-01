#0PB7QVJ9Z7XQB4T8
import pandas as pd
import numpy as np
import requests
import io
import csv

def API_intraday(ticker,interval):
    url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval='+str(interval)+'min&apikey=0PB7QVJ9Z7XQB4T8&datatype=csv'
    var=requests.get(url)
    df = pd.read_csv(io.StringIO(var.text), sep=',', quoting=csv.QUOTE_ALL)
    # with pd.option_context(
    #         'display.width', None,
    #         'display.max_columns', None,
    #         'display.max_colwidth', -1,
    #         'display.colheader_justify', 'left'):
    #     print(df)

    return df

def API_search_ticker(text):
    url='https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=0PB7QVJ9Z7XQB4T8'
    var=requests.get(url)
    df = pd.read_csv(io.StringIO(var.text), sep=',', quoting=csv.QUOTE_ALL)
    df["Indexes"] = df["name"].str.contains(text, case=False)
    df1 = df[(df['Indexes'] == True)]
    print(df1)
    return


ticker_dict={}
ticker='IBM'
#ticker_dict.update ({ticker:API_intraday(ticker,5)})
#print(ticker_dict)

API_search_ticker('microsoft')