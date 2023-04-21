from flask import Flask, render_template, request
import requests
import datetime
import time
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/')
def index():
    # API endpoint for getting the top 10 highest priced cryptocurrencies
    api_endpoint = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&locale=en'
    
    # Make a GET request to the API endpoint and get the response in JSON format
    response = requests.get(api_endpoint)
    data = response.json()
    
    # Extract the name and price of each cryptocurrency and store it in a list
    crypto_data = []
    for currency in data:
        id = currency['id']
        name = currency['id']
        price = currency['current_price']
        crypto_data.append((name, price, id))
    
    # Render the template with the data
    return render_template('index.html', crypto_data=crypto_data)

@app.route('/search',methods=['POST'])
def search():
    if request.method == "POST":
        crypto = request.form.get('crypto')
        api_endpoint = f'https://api.coingecko.com/api/v3/search?query={crypto}'
        api_endpoint.format(crypto)
        response = requests.get(api_endpoint)
        data = response.json()
        crypto_data = []
        for currency in data['coins']:
            id = currency['id']
            name = currency['name']
            symbol = currency['symbol']
            crypto_data.append((name,symbol,id))
        return render_template('search.html',crypto_data=crypto_data)

@app.route('/coin/detail/<id>')
def detail(id):
    now = datetime.datetime.now()
    unix_now = time.mktime(now.timetuple())
    previous_month = now - relativedelta(months=1)
    unix_previous = time.mktime(previous_month.timetuple())
    coin_id = id
    api_endpoint = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={unix_previous}&to={unix_now}'
    response = requests.get(api_endpoint)
    data = response.json()
    for dt in data['prices']:
        dt[0] = str(dt[0])[:-3]
    #     dt[0] = str(datetime.datetime.utcfromtimestamp(int(dt[0])).strftime('%Y-%m-%d'))
    data = data['prices']
    print(data)
    return render_template('detail.html',data=data,coin_id=coin_id)

if __name__ == '__main__':
    app.run(debug=True)