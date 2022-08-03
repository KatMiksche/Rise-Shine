from RSSQL import connection

def test_connection():
    con = connection()
    assert con

def test_database_exists():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("use RISESHINE;")
    assert mycursor

def test_database_ok():
    con = connection()
    mycursor = con.cursor()
    mycursor.execute("select * from information_schema.tables where table_schema='riseshine';")
    tables=mycursor.fetchall()
    assert len(tables)==4
