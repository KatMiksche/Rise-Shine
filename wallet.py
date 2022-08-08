import pandas as pd
from RSSQL import *

class wllt():
    def __init__(self):
        self.curvalue=0

    def CurrentValue(self,cursor):
        cursor.execute("select CurrentWallet from wallet order by date desc limit 1;")
        value=cursor.fetchall()
        value=str(value[0])
        self.curvalue=float(value[10:-4])
        return self.curvalue

    def ShowRecords(self,cursor):
        cursor.execute("select * from wallet order by Date desc;")
        records=pd.DataFrame(cursor.fetchall())
        records.columns = ['Value','Change','Timestamp','Comment']
        return records

    def WriteRecord(self,cursor, change, text):
        NewValue=self.CurrentValue(cursor)+change
        data=[NewValue, change, text]
        cursor.execute('INSERT INTO wallet (CurrentWallet, ValueChange, Description) VALUES(%s, %s, %s)',
                       data)
        self.CurrentValue(cursor)

if __name__ == "__main__":
    pass