from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from stockhelper.alphaQuery import AlphaQuery
import json
# Create your views here.


# returns json time series data for the requested stock and the requested interval
def getStockData(request,ticker,interval):
    print(interval)
    print(ticker)
    if interval in ['1min', '5min', '15min', '30min', '60min']:
        intraday=True
    else:
        intraday=False
    print(intraday)
    data = AlphaQuery(ticker,intraday,interval).run()
    return JsonResponse({'data':data})

def getStockDataForCharting(request,ticker,interval):
    if interval in ['1min', '5min', '15min', '30min', '60min']:
        intraday=True
    else:
        intraday=False
    print(intraday)
    data = AlphaQuery(ticker,intraday,interval).run()
    ret_data = []
    for quote in data:
        time = int(quote['openTime'].timestamp()*1000)
        o = float(quote['open'])
        h = float(quote['high'])
        l = float(quote['low'])
        c = float(quote['close'])
        ret_data += [[time,o,h,l,c]]
    return JsonResponse(list(reversed(ret_data)),safe=False)

def index(request):
    return render(request, "index.html")
