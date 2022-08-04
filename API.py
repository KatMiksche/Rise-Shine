from flask import *
from main import *
from RSSQL import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

con, mycursor = DBconnection(config(), False)
portfolios_dict = fetch_portfolios(mycursor)
load_portfolios(portfolios_dict, mycursor)
DBend(con,mycursor)

@app.route('/',methods=['GET'])
def home():
    data=['/portfolios - for list of portfolios, their names and current values',\
          '/portfolio_detail/<int:id> - for detail of portfolio returning id, name, current value, content of portfolio'\
          'and list of historic values',\
          '/stock/<ticker>/<int:interval> - for data about stock, supported intervals: 1min, 5min, 15min, 30min, 60min',\
          '/stock_current/<ticker> - for actual price of ticker']
    return data

@app.route('/portfolios',methods=['GET'])
def portfolios():
    return jsonify(portfolios_overview(portfolios_dict))

@app.route('/portfolio_detail/<int:id>', methods=['GET'])
def portfolio_detail(id):
    data={'ID':portfolios_dict[id].id, \
          'NAME': portfolios_dict[id].name, \
          'CURRENT VALUE':portfolios_dict[id].current_value, \
          'HOLD': portfolios_dict[id].hold.tolist(), \
          'HISTORIC VALUE': portfolios_dict[id].historic_value.tolist()}
    return jsonify(data)

@app.route('/stock/<ticker>/<int:interval>', methods=['GET'])
def stock(ticker,interval):
    return jsonify(API_intraday(ticker,interval).to_dict())

@app.route('/stock_current/<ticker>', methods=['GET'])
def stock_current(ticker):
    return jsonify(API_current_price(ticker))

if __name__ == '__main__':
    app.run(debug=True)