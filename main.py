from exAPI import *
from RSSQL import connection
from wallet import wllt
import pandas as pd
from portfolio import prtfl

def fetch_portfolios(cursor):
    dictionary={}
    cursor.execute("select portfolioid from portfolio;")
    records = cursor.fetchall()
    for i in range(len(records)):
        var=i+1
        dictionary.update({var:prtfl(var)})
    return dictionary

def initial_check():
    pass

def load_portfolios(dictionary,cursor):
    dictionary = fetch_portfolios(cursor)
    for i in range(len(dictionary)):
        var = i + 1
        dictionary[var].SQL_load(cursor)
        dictionary[var].update(cursor)

def start_portfolio():
    pass

wallet=wllt
tickers= pd.DataFrame
#tickers=API_get_tickers()

con = connection()
con.autocommit = True
mycursor = con.cursor()
mycursor.execute("use RISESHINE;")



# inicialize portfolios, load and update
portfolios_dict = fetch_portfolios(mycursor)
load_portfolios(portfolios_dict,mycursor)


mycursor.close()
con.close()