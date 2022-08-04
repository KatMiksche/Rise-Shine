from exAPI import *
from RSSQL import *
from wallet import wllt
from portfolio import prtfl
import pandas as pd

def fetch_portfolios(cursor):
    dictionary={}
    cursor.execute("select portfolioid from portfolio;")
    records = cursor.fetchall()
    for i in range(len(records)):
        var=(records[i])[0]
        dictionary.update({var:prtfl(var)})
    return dictionary



def load_portfolios(dictionary,cursor):
    keys=list(dictionary.keys())
    for i in range(len(dictionary)):
        var = keys[i]
        dictionary.update({var:dictionary[var].SQL_load(cursor)})
        dictionary.update({var:dictionary[var].update_records(cursor)})
    return True

def start_portfolio(name,dictionary,cursor):
    data=[name]
    cursor.execute('insert into portfolio (name) values (%s);', data)
    newdict=fetch_portfolios(cursor)
    newdict=list(newdict.keys())
    var=newdict[-1]
    dictionary.update({var: prtfl(var)})
    dictionary[var].SQL_load(cursor)
    message='portfolio '+str(var)+': '+name+' successfully created'
    return message

def portfolios_overview(dictionary):
    overview=[]
    keys = list(dictionary.keys())
    for i in range(len(dictionary)):
        var = keys[i]
        overview.append([dictionary[var].id, dictionary[var].name, dictionary[var].current_value])
    return overview


if __name__ == "__main__":
    wallet123=wllt()
    tickers= pd.DataFrame
    #tickers=API_get_tickers()

    con, mycursor = DBconnection(config(),True)

    # inicialize portfolios, load and update
    portfolios_dict = fetch_portfolios(mycursor)
    print(portfolios_overview(portfolios_dict))
    load_portfolios(portfolios_dict,mycursor)
    print(portfolios_overview(portfolios_dict))
    # print(portfolios_dict)
    # print(portfolios_overview(portfolios_dict))

    #print(portfolios_dict[6].historic_value)
    # portfolios_dict[6].buy(mycursor,wallet123,'AAPL',10)
    # portfolios_dict[6].print()

    #print(start_portfolio('tech stock',portfolios_dict,mycursor))
    #print(portfolios_dict)
    # print(portfolios_dict[6].historic_value)
    #print(portfolios_overview(portfolios_dict))
    #portfolios_dict[1].print()
    #portfolios_dict[6].graph_performance(mycursor)


    #DBend(con, mycursor)