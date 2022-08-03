import numpy
from RSSQL import connection
from wallet import wllt

def test_current_value():
    wallet = wllt
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use riseshine;")
    var=wallet.CurrentValue(wallet,mycursor)
    assert type(var) == float
    mycursor.close()
    con.close()

def test_show_records():
    wallet = wllt
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use riseshine;")
    var=wallet.ShowRecords(wallet, mycursor)
    assert type(var) == numpy.ndarray
    mycursor.close()
    con.close()

def test_write_record():
    wallet = wllt
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use riseshine;")
    before=wallet.CurrentValue(wallet,mycursor)
    wallet.WriteRecord(wallet, mycursor, 0.99, 'TEST')
    before=round(before+0.99,2)
    assert wallet.CurrentValue(wallet,mycursor)==before
    mycursor.close()
    con.close()
