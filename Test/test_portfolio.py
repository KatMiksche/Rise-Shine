from portfolio import prtfl
from RSSQL import connection
from wallet import wllt

def test_print():
    portfolio=prtfl(1)
    assert portfolio.print()


def test_load_hold():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id=mycursor.fetchall()
    id=id[0]
    id=id[0]
    data=['IBM',100,id]
    mycursor.execute('insert into hold (ticker, volume, portfolioid) values (%s, %s, %s)',data)
    portfolio=prtfl(id)
    portfolio.load_hold(mycursor)
    assert portfolio.hold.size != 0
    mycursor.close()
    con.close()

con = connection()
#con.autocommit = True
mycursor = con.cursor()
mycursor.execute("use RISESHINE;")
mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
var=mycursor.fetchall()
print(var)
print(type(var))

def test_load_name():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id=mycursor.fetchall()
    id=id[0]
    id=id[0]
    portfolio=prtfl(id)
    portfolio.load_name(mycursor)
    assert portfolio.name == 'pytest portfolio'
    mycursor.close()
    con.close()


def test_load_currentvalue():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id = mycursor.fetchall()
    id = id[0]
    id = id[0]
    data = ['IBM', 100, id]
    mycursor.execute('insert into hold (ticker, volume, portfolioid) values (%s, %s, %s)', data)
    portfolio = prtfl(id)
    portfolio.load_currentvalue(mycursor)
    assert portfolio.current_value > 0
    mycursor.close()
    con.close()


def test_load_historicvalue():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id = mycursor.fetchall()
    id = id[0]
    id = id[0]
    portfolio = prtfl(id)
    portfolio.load_historicvalue(mycursor)
    assert portfolio.historic_value.size != 0
    mycursor.close()
    con.close()


def test_sql_load():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id = mycursor.fetchall()
    id = id[0]
    id = id[0]
    data = ['IBM', 100, id]
    mycursor.execute('insert into hold (ticker, volume, portfolioid) values (%s, %s, %s)', data)
    portfolio = prtfl(id)
    portfolio.SQL_load(mycursor)
    assert portfolio.hold.size != 0 and portfolio.historic_value.size != 0 and portfolio.current_value > 0 \
           and portfolio.name == 'pytest portfolio'
    mycursor.close()
    con.close()


def test_graph_performance():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id = mycursor.fetchall()
    id = id[0]
    id = id[0]
    portfolio = prtfl(id)
    graph=portfolio.graph_performance(mycursor)
    assert graph
    mycursor.close()
    con.close()


def test_buy():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    mycursor.execute("""insert into portfolio (name) values ('pytest portfolio');""")
    mycursor.execute("""select portfolioid from portfolio where name = 'pytest portfolio';""")
    id = mycursor.fetchall()
    id = id[0]
    id = id[0]
    mywallet=wllt()
    portfolio = prtfl(id)
    graph = portfolio.graph_performance(mycursor)
    assert graph
    mycursor.close()
    con.close()


def test_sell():
    assert False


def test_close():
    assert False


def test_get_historic_data():
    assert False


def test_insert_historic_values():
    assert False


def test_update_records():
    assert False
