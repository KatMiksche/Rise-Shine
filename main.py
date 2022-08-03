from exAPI import *
from RSSQL import connection
from wallet import wllt
import pandas as pd
from portfolio import prtfl
import importlib as imp


def fetch_portfolios(cursor):
    dictionary={}
    cursor.execute("select portfolioid from portfolio;")
    records = cursor.fetchall()
    for i in range(len(records)):
        var=i+1
        dictionary.update({var:prtfl(var)})
    return dictionary



def load_portfolios(dictionary,cursor):
    dictionary = fetch_portfolios(cursor)
    for i in range(len(dictionary)):
        var = i + 1
        dictionary.update({var:dictionary[var].SQL_load(cursor)})
        dictionary.update({var:dictionary[var].update_records(cursor)})
    return dictionary

def start_portfolio(name,dictionary,cursor):
    data=[name]
    cursor.execute('insert into portfolio (name) values (%s);', data)
    var=list(dictionary)[-1]
    var=var+1
    dictionary.update({var: prtfl(var)})
    dictionary[var].SQL_load(cursor)
    message='portfolio '+str(var)+': '+name+' successfully created'
    return message

def portfolios_overview(dictionary):
    overview=[]
    for i in range(len(dictionary)):
        var = i + 1
        overview.append([dictionary[var].id, dictionary[var].name, dictionary[var].current_value])
    return overview



wallet123=wllt
tickers= pd.DataFrame
#tickers=API_get_tickers()

con = connection()
con.autocommit = True
mycursor = con.cursor()
mycursor.execute("use RISESHINE;")

# inicialize portfolios, load and update
portfolios_dict = fetch_portfolios(mycursor)
portfolios_dict=load_portfolios(portfolios_dict,mycursor)
print(portfolios_dict)
print(portfolios_overview(portfolios_dict))

#print(portfolios_dict[6].historic_value)
portfolios_dict[6].buy(mycursor,wallet123,'AAPL',10)
portfolios_dict[6].print()

#print(start_portfolio('vsechno nove trojka',portfolios_dict,mycursor))
#print(portfolios_dict)
# print(portfolios_dict[6].historic_value)
#print(portfolios_overview(portfolios_dict))
#portfolios_dict[1].print()
#portfolios_dict[6].graph_performance(mycursor)



# mycursor.close()
# con.close()