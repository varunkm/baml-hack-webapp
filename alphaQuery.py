import requests
import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bamlhacksite.settings")
import django
django.setup()
from stockhelper.models import StockQuote

class AlphaQuery:
    def __init__(self,ticker,intraday,period):
        self.ticker   = ticker
        self.intraday = intraday
        self.period = period
        self.API_KEY = ''
        with open('alphavantage.key') as secret:
            self.API_KEY = secret.readline(16)
    def run(self):
        base_url = 'https://www.alphavantage.co/query?function='
        if self.intraday:
            if self.period not in ['1min', '5min', '15min', '30min', '60min']:
                print('period must be 1min, 5min, 15min, 30min or 60min')
                return
            base_url += 'TIME_SERIES_INTRADAY'
            base_url += '&interval='+self.period
        else:
            if self.period not in ['daily','weekly','monthly']:
                print('period must be daily, weekly or monthly')
                return
            base_url += 'TIME_SERIES_'+self.period.upper()+'_ADJUSTED'
            base_url += '&outputsize=full'
        base_url += '&symbol='+self.ticker
        base_url += '&apikey='+self.API_KEY
        r = requests.get(base_url)

        period_copy =  self.period if self.intraday else self.period.title()

        data = r.json()['Time Series ('+self.period+')']
        for obj in data:
            time = datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
            quote = data[obj]
            #{'1. open': '82.4150', '2. high': '82.4300', '3. low': '82.4000', '4. close': '82.4000', '5. volume': '30079'}
            openP = quote['1. open']
            highP = quote['2. high']
            lowP  = quote['3. low']
            closeP = quote['4. close']
            vol = quote['5. volume']
            q = StockQuote(company=self.ticker,risk='high',openTime=time,highPrice=highP,lowPrice=lowP,openPrice=openP,closePrice=closeP,volume=vol,period='1min')
            print(q)
            q.save()
