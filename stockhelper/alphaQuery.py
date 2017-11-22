import requests
import os
import datetime
import pandas as pd
import json

class AlphaQuery:
    def __init__(self,ticker,intraday,period):
        self.ticker   = ticker
        self.intraday = intraday
        self.period = period
        self.API_KEY = ''
        with open('alphavantage.key') as secret:
            self.API_KEY = secret.readline(16)

    def getPandas(self):
        def datetime_handler(x):
            if isinstance(x, datetime.datetime):
                return x.isoformat()
            raise TypeError("Unknown type")

        quotes = self.run()
        df = pd.read_json(json.dumps(quotes, default=datetime_handler))
        df['DateTime'] = pd.to_datetime(df['openTime'])
        df.set_index('DateTime', inplace=True)
        del df['openTime']
        return df

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
            base_url += 'TIME_SERIES_'+self.period.upper()
            base_url += '&outputsize=full'
        base_url += '&symbol='+self.ticker
        base_url += '&apikey='+self.API_KEY
        r = requests.get(base_url)

        period_copy =  self.period if self.intraday else self.period.title()
        what_we_dont_want = 'Meta Data'
        what_we_want = [key for key in r.json().keys() if key != what_we_dont_want]
        data = r.json()[what_we_want[0]]
        quotes = []
        for obj in data:
            if len(obj) == 10:
                time = datetime.datetime.strptime(obj, "%Y-%m-%d")
            else:
                time = datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
            quote = data[obj]
            #{'1. open': '82.4150', '2. high': '82.4300', '3. low': '82.4000', '4. close': '82.4000', '5. volume': '30079'}
            openP = quote['1. open']
            highP = quote['2. high']
            lowP  = quote['3. low']
            closeP = quote['4. close']
            vol = quote['5. volume']
            new_quote = {
                'ticker':self.ticker,
                'period':self.period,
                'openTime':time,
                'open':openP,
                'close':closeP,
                'high':highP,
                'low':lowP,
                'vol':vol
            }
            quotes+=[new_quote]
        return quotes
