from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from stockhelper.alphaQuery import AlphaQuery
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
