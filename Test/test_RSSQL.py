from RSSQL import *

def test_connection_and_database_exists():
    con, mycursor = DBconnection(config(),False)
    assert con
    DBend(con,mycursor)

def test_database_ok():
    con, mycursor = DBconnection(config(),False)
    mycursor.execute("select * from information_schema.tables where table_schema='riseshine';")
    tables=mycursor.fetchall()
    assert len(tables)==4
    DBend(con,mycursor)
