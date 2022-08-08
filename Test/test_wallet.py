import pandas
from RSSQL import *
from wallet import wllt

def test_current_value():
    wallet = wllt()
    con, mycursor = DBconnection(config(),False)
    var=wallet.CurrentValue(mycursor)
    assert type(var) == float
    DBend(con,mycursor)

def test_show_records():
    wallet = wllt()
    con, mycursor = DBconnection(config(),False)
    var=wallet.ShowRecords(mycursor)
    assert type(var) == pandas.core.frame.DataFrame
    DBend(con,mycursor)

def test_write_record():
    wallet = wllt()
    con, mycursor = DBconnection(config(),False)
    before=wallet.CurrentValue(mycursor)
    wallet.WriteRecord(mycursor, 0.99, 'TEST')
    assert wallet.CurrentValue(mycursor)>before
    DBend(con,mycursor)
