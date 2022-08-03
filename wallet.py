from RSSQL import connection
import numpy as np
from itertools import chain

class wllt():
    def __init__(self):
        self.curvalue=0


    def CurrentValue(self,cursor):
        cursor.execute("select CurrentWallet from wallet order by date desc limit 1;")
        value=cursor.fetchall()
        value=str(value[0])
        value=float(value[10:-4])
        self.curvalue=value
        return value

    def ShowRecords(self,cursor):
        cursor.execute("select * from wallet order by Date desc;")
        records=cursor.fetchall()
        data_type = [('CurrentValue', float),
                     ('Change', float),
                     ('Date', str, 20),
                     ('Description', str, 255)]
        records = np.fromiter(records, count=len(records), dtype=data_type)
        return records

    def WriteRecord(self,cursor, change, text):
        NewValue=self.CurrentValue(cursor)+change
        data=[NewValue, change, text]
        cursor.execute('INSERT INTO wallet (CurrentWallet, ValueChange, Description) VALUES(%s, %s, %s)',
                       data)


# wallet=wllt
# con = connection()
# con.autocommit=True
# mycursor = con.cursor()
# mycursor.execute("use riseshine;")
# print(type(wallet.ShowRecords(wallet,mycursor)))