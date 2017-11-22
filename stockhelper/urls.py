from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quote/(?P<ticker>[A-Z]+)/(?P<interval>[a-zA-Z0-9]+)/$', views.getStockData, name='stockQuoteJson'),
    url(r'^chart/(?P<ticker>[A-Z]+)/(?P<interval>[a-zA-Z0-9]+)/$', views.getStockDataForCharting, name='stockQuoteChart'),
    url(r'^stock/(?P<ticker>[A-Z]+)/(?P<sharpe>.+)/(?P<alpha>.+)/(?P<beta>.+)/(?P<std_dev>.+)$', views.getStockDetailView, name='stockDetail'),
    url(r'^generate/$', views.generatePortfolio, name='generatePortfolio'),
    url(r'^signup/$', views.register, name='register')

]
