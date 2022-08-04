from main import *
from Test.test_portfolio import get_new_portf_id, input_data
from RSSQL import *

def test_fetch_portfolios():
    con, mycursor = DBconnection(config(),False)
    get_new_portf_id(mycursor)
    dict=fetch_portfolios(mycursor)
    assert len(dict)>0
    DBend(con,mycursor)

def test_load_portfolios():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor)
    dict=fetch_portfolios(mycursor)
    load_portfolios(dict,mycursor)
    assert dict[id].name != ''
    DBend(con,mycursor)

def test_start_portfolio():
    con, mycursor = DBconnection(config(),False)
    dict=fetch_portfolios(mycursor)
    start_portfolio('main test portfolio',dict,mycursor)
    keys=list(dict.keys())
    assert dict[keys[-1]].name == 'main test portfolio'
    DBend(con,mycursor)

def test_portfolios_overview():
    con, mycursor = DBconnection(config(),False)
    get_new_portf_id(mycursor)
    dict = fetch_portfolios(mycursor)
    load_portfolios(dict,mycursor)
    assert len(portfolios_overview(dict))>0
    DBend(con,mycursor)