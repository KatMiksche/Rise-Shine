from RSSQL import connection

def test_connection():
    con = connection()
    assert con
    con.close()

def test_database_exists():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    assert mycursor
    mycursor.close()
    con.close()

def test_database_ok():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("select * from information_schema.tables where table_schema='riseshine';")
    tables=mycursor.fetchall()
    assert len(tables)==4
    mycursor.close()
    con.close()
