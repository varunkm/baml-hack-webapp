from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from stockhelper.alphaQuery import AlphaQuery
import json
from stockhelper.calculations import get_risk_indicators
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

# gets stock price data in the format required for highstock
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

def getStockDetailView(request,ticker, sharpe,alpha, beta, std_dev):
    return render(request,'stockdetail.html',{'ticker':ticker, 'sharpe':sharpe, 'alpha':alpha, 'beta':beta, 'std_dev':std_dev})

# helper functions
def createPortfolio(risk,cash):
    assets = {
    'HIGH':["APC","MS","DVN"],
    'MED': ["EMR","FOXA","UNH"],
    'LOW': ["SO","PG","EXC"]}
    my_port = assets[risk]

    def getLatestPrice(ticker):
        data = AlphaQuery(ticker,True,'1min').run()
        #print(ticker,data)
        return  float(data[0]['close'])
    prices = [getLatestPrice(stock) for stock in my_port]
    avg_alloc = float(cash)/len(prices)
    quans = [int(avg_alloc/ price ) for price in prices]
    cons  = [price*quan for (price,quan) in zip(prices,quans)]
    return zip(my_port,prices,quans,cons)

def calcPortfolioRisk(portfolio):
    benchmark = 'SPY'
    inputs_to_risk = []
    for ticker,price,quan,cons in portfolio:
        prices_df = AlphaQuery(ticker,False,'daily').getPandas()
        inputs_to_risk += [(prices_df,ticker,quan)]
    sandp500 = AlphaQuery(benchmark,False,'daily').getPandas()
    inputs_to_risk+=[(sandp500,)]
    return (get_risk_indicators(inputs_to_risk))

def generatePortfolio(request):
    risk = request.POST.get("risk")
    cash = request.POST.get("cash")
    print('generate port',risk,cash)

    portfolio = list(createPortfolio(risk,cash))

    print('generated port',portfolio)
    risk_metrics = calcPortfolioRisk(portfolio)
    return render(request,'portfolio.html',{'test':'test','portfolio':portfolio,'risk_metrics':risk_metrics})

def register(request):
    return render(request,'signup.html')

def index(request):
    return render(request, "index.html")
