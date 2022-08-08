from portfolio import prtfl
from RSSQL import *
from wallet import wllt

con, mycursor = DBconnection(config(),False)

# help functions for testing
def get_new_portf_id(cursor, name):
    cursor.execute("""
    insert into portfolio (name) values (%s);""", [name])
    cursor.execute("""
    select portfolioid from portfolio where name = %s;""",[name])
    id = cursor.fetchall()
    id = (id[0])[0]
    return id

def input_data(cursor,id):
    data = ['IBM', 100, id]
    cursor.execute('insert into hold (ticker, volume, portfolioid) values (%s, %s, %s)', data)

# test functions
def test_print():
    portfolio=prtfl(1)
    assert portfolio.print()

def test_load_hold():
    con, mycursor = DBconnection(config(), False)
    id=get_new_portf_id(mycursor,'pytest hold')
    input_data(mycursor,id)
    portfolio=prtfl(id)
    portfolio.load_hold(mycursor)
    assert portfolio.hold.size != 0
    DBend(con, mycursor)

def test_load_name():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor, 'pytest portfolio')
    portfolio=prtfl(id)
    portfolio.load_name(mycursor)
    assert portfolio.name == 'pytest portfolio'
    DBend(con,mycursor)

def test_load_currentvalue():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor,'pytest value')
    input_data(mycursor,id)
    portfolio = prtfl(id)
    portfolio.load_currentvalue(mycursor)
    assert portfolio.current_value > 0
    DBend(con,mycursor)

def test_load_historicvalue():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor,'pytest hist value')
    portfolio = prtfl(id)
    portfolio.load_historicvalue(mycursor)
    assert portfolio.historic_value.size != 0
    DBend(con,mycursor)

def test_sql_load():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor, 'pytest sql load')
    input_data(mycursor,id)
    portfolio = prtfl(id)
    portfolio.SQL_load(mycursor)
    assert portfolio.hold.size!=0 and portfolio.historic_value.size!=0 and portfolio.current_value>0 \
           and portfolio.name=='pytest sql load'
    DBend(con,mycursor)

def test_graph_performance():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor,'pytest graph')
    portfolio = prtfl(id)
    graph, path=portfolio.graph_performance(mycursor)
    assert graph
    DBend(con,mycursor)

def test_buy():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor,'pytest buy')
    mywallet=wllt()
    mywallet.WriteRecord(mycursor,10000,'test funds')
    portfolio = prtfl(id)
    portfolio.buy(mycursor,mywallet,'IBM',1)
    assert portfolio.hold.size != 0
    DBend(con,mycursor)

def test_sell():
    con, mycursor = DBconnection(config(),False)
    id=get_new_portf_id(mycursor,'pytest sell')
    input_data(mycursor,id)
    mywallet=wllt()
    portfolio = prtfl(id)
    portfolio.sell(mycursor,mywallet,'IBM',100)
    assert portfolio.hold.size == 0
    DBend(con,mycursor)

def test_close():
    con, mycursor = DBconnection(config(),False)
    id = get_new_portf_id(mycursor,'pytest close')
    input_data(mycursor, id)
    mywallet = wllt()
    portfolio = prtfl(id)
    portfolio.close(mycursor,mywallet)
    assert portfolio.hold.size == 0
    DBend(con,mycursor)

def test_get_historic_data():
    con, mycursor = DBconnection(config(),False)
    id = get_new_portf_id(mycursor,'pytest get historic data')
    input_data(mycursor, id)
    portfolio = prtfl(id)
    portfolio.load_hold(mycursor)
    data=portfolio.get_historic_data()
    assert data.size>199
    DBend(con,mycursor)

def test_insert_historic_values():
    con, mycursor = DBconnection(config(),False)
    id = get_new_portf_id(mycursor,'pytest insert hist value')
    input_data(mycursor, id)
    portfolio = prtfl(id)
    portfolio.load_hold(mycursor)
    historic_data = portfolio.get_historic_data()
    data=[id]
    mycursor.execute("""update value set date='2022-07-25' where portfolioid=%s;""",data)
    portfolio.insert_historic_values(mycursor,5,historic_data)
    portfolio.load_historicvalue(mycursor)
    assert portfolio.historic_value.size == 7
    DBend(con,mycursor)

def test_update_records():
    con, mycursor = DBconnection(config(),False)
    id = get_new_portf_id(mycursor,'pytest update records')
    input_data(mycursor, id)
    portfolio = prtfl(id)
    portfolio.load_hold(mycursor)
    data = [id]
    mycursor.execute("""update value set date='2022-07-25' where portfolioid=%s;""", data)
    portfolio.update_records(mycursor)
    assert portfolio.historic_value.size > 1
    DBend(con, mycursor)

DBend(con,mycursor)
