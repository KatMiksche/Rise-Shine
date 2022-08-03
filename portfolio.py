import pandas as pd
import plotly.express as px
from exAPI import API_daily, API_current_price
from RSSQL import connection
import numpy as np
from wallet import wllt
from datetime import datetime

class prtfl:
    def __init__(self,PortfolioID):
        self.id=PortfolioID
        self.name=''
        self.hold=np.array([])
        self.historic_value=np.array([])
        self.current_value=0

    def print(self):
        print('ID: ',self.id)
        print('name: ',self.name)
        print('current value: ',self.current_value)
        np.set_printoptions(threshold=None, edgeitems=1, linewidth=6)
        print('hold: ',self.hold, sep='\n')
        print('value: ',self.historic_value, sep='\n')
        return True

    def load_hold(self,cursor):
        data=[self.id]
        cursor.execute("select ticker,volume, value from hold where portfolioid=%s;",data)
        records = cursor.fetchall()
        data_type = [('Ticker', str, 5),
                     ('Volume', int),
                     ('Value', float)]
        self.hold = np.fromiter(records, count=len(records), dtype=data_type)
        return self.hold

    def load_name(self,cursor):
        data = [self.id]
        cursor.execute("select Name from portfolio where portfolioid=%s;",data)
        value = cursor.fetchall()
        value = str(value[0])
        self.name = value[2:-3]
        return self.name

    def load_currentvalue(self,cursor):
        self.current_value=0
        for i in range(len(self.hold)):
            ticker=self.hold[i][0]
            volume=self.hold[i][1]
            tickervalue=API_current_price(ticker)
            data = [tickervalue, ticker, self.id]
            cursor.execute('UPDATE hold set Value=%s where ticker=%s and portfolioid=%s;', data)
            self.current_value=self.current_value+(volume*tickervalue)
        data=[self.current_value, self.id]
        cursor.execute('update portfolio set value=%s where portfolioid=%s;',data)
        return self.current_value

    def load_historicvalue(self,cursor):
        data = [self.id]
        cursor.execute("select date, value, difference from value where portfolioid=%s order by date asc;", data)
        records = cursor.fetchall()
        data_type = [('Date', str, 20),
                     ('Value', float),
                     ('Difference', float)]
        self.historic_value = np.fromiter(records, count=len(records), dtype=data_type)
        return self.historic_value

    def SQL_load(self,cursor):
        self.load_name(cursor)
        self.load_hold(cursor)
        self.load_currentvalue(cursor)
        self.load_historicvalue(cursor)
        print('load successful')
        return self

    def graph_performance(self,cursor):
        self.load_currentvalue(cursor)
        if self.historic_value.size == 0: self.load_historicvalue(cursor)
        text='Portfolio '+str(self.id)+': '+self.name+', current value: $'+str(self.current_value)
        graph = px.line(self.historic_value, x="Date", y="Value", markers=True, hover_data=["Difference"])
        graph.update_layout(title={'text': text, 'x': 0.5})
        graph.show()
        return graph

    def buy(self,cursor,user_wallet, ticker,volume):
        if self.hold.size == 0: self.load_hold(cursor)
        ticker_price=API_current_price(ticker)
        price=volume*ticker_price
        funds=user_wallet().CurrentValue(cursor)
        if price>funds:
            message='insufficient funds, purchase not made'
        else:
            price=-price
            text='Purchase of '+str(volume)+' stocks of '+ticker
            user_wallet().WriteRecord(cursor, price, text)
            if ticker in self.hold['Ticker']:
                data = [volume,ticker,self.id]
                cursor.execute('UPDATE hold set Volume=Volume+%s where ticker=%s and portfolioid=%s;',data)
            else:
                data = [ticker, volume, self.id, ticker_price]
                cursor.execute('INSERT INTO hold (ticker, volume, portfolioid, value) VALUES(%s, %s, %s, %s);',data)
            self.load_hold(cursor)
            self.load_currentvalue(cursor)
            message='purchase successfully made'
        print(message)
        return self

    def sell(self,cursor,user_wallet, ticker,volume):
        if self.hold.size == 0: self.load_hold(cursor)
        if ticker not in self.hold['Ticker']:
            message='you do not own any stocks of this ticker'
        else:
            var=np.where(self.hold['Ticker'] == ticker)
            var=int(var[0])
            if self.hold[var][1]<volume:
                message='you do not have enough stocks of this ticker'
            else:
                price = volume * API_current_price(ticker)
                data = [volume, ticker, self.id]
                cursor.execute('UPDATE hold set Volume=Volume-%s where ticker=%s and portfolioid=%s;', data)
                text = 'Sale of ' + str(volume) + ' stocks of ' + ticker
                user_wallet().WriteRecord(cursor, price, text)
                cursor.execute('DELETE FROM HOLD WHERE Volume=0;')
                self.load_hold(cursor)
                self.load_currentvalue(cursor)
                message = 'sale successfully made'
        print(message)
        return self

    def close(self,cursor, wallet):
        var=len(self.hold)
        for i in range(var):
            ticker=str(self.hold[0][0])
            volume=int(self.hold[0][1])
            self.sell(cursor,wallet,ticker,volume)
        message='portfolio closure was successful'
        return message

    def get_historic_data(self):
        historic_records = pd.DataFrame()
        for i in range(len(self.hold)):
            ticker = self.hold[i][0]
            data = API_daily(ticker)
            data = data.drop(['open', 'high', 'low', 'volume'], axis=1)
            data = data.rename(columns={"close": ticker})
            if historic_records.empty:
                historic_records = data
            else:
                historic_records = historic_records.merge(data, on='timestamp')
        return historic_records

    def insert_historic_values(self,cursor,days,historic_records):
        for i in range(days, -1, -1):
            value = 0
            date = historic_records.at[i, 'timestamp']
            #print('updating date ', date)
            for j in range(len(self.hold)):
                ticker = self.hold[j][0]
                volume = self.hold[j][1]
                tickervalue = historic_records.at[i, ticker]
                value = value + (volume * tickervalue)
                #print(ticker, volume, tickervalue, value)
            data = [self.id, date, value]
            cursor.execute('insert into value (portfolioid, date, value) values (%s,%s,%s);', data)

    def update_records(self,cursor):
        if self.historic_value.size==0 or self.hold.size==0: self.SQL_load(cursor)
        #if self.hold.size==0: self.SQL_load(cursor)
        lastdate=str(self.historic_value[-1][0])
        lastdate=datetime.strptime(lastdate[2:],'%y-%m-%d')
        difference=datetime.now()-lastdate
        #print('difference of days ',difference)
        if difference.days>1:
            historic_records=self.get_historic_data()
            days_required=historic_records.loc[historic_records['timestamp'] == str(self.historic_value[-1][0])].index[0]
            days_required=days_required-1
            self.insert_historic_values(cursor,days_required,historic_records)
            self.load_historicvalue(cursor)
            #print(self.historic_value)
            message='update successful'
        else:
            message='update not required'
        print(message)
        return self


# con = connection()
# con.autocommit = True
# mycursor = con.cursor()
# mycursor.execute("use RISESHINE;")
#
# wallet=wllt()
# portfolio1=prtfl(1)
# portfolio2=prtfl(2)
# portfolio1.SQL_load(mycursor)
# print(portfolio1.update(mycursor))

# print(portfolio2.close(mycursor,wallet))
# print(portfolio2.hold)
# print(portfolio2.current_value)

#print(portfolio1.sell(mycursor,wallet,'IBM',50))
# print(API_current_price(ticker))
# print(portfolio2.buy(mycursor,wallet,ticker,25))
# print(wallet.CurrentValue(mycursor))
# print(portfolio2.hold)
# print(portfolio2.current_value)
#portfolio1.load_currentvalue(mycursor)
#portfolio1.graph_performance(mycursor)

#portfolio1.load_hold(mycursor)
#portfolio1.load_currentvalue(mycursor)
#portfolio2.load(mycursor)
#print('IBM ',API_current_price('IBM'))
#print('MSFT ',API_current_price('MSFT'))
#print('p1 hold ',portfolio1.hold)
#print('p1 value ',portfolio1.currentvalue)
# print('p2 hold ',portfolio2.hold)
# print('p2 value ',portfolio2.currentvalue)
#print(portfolio1)
# print(portfolio1.load_value(mycursor))
# print(portfolio2.load_value(mycursor))
# print(type(portfolio2.load_value(mycursor)))
#portfolio1.print()

# mycursor.close()
# con.close()

