from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quote/(?P<ticker>[A-Z]+)/(?P<interval>[a-zA-Z0-9]+)/$', views.getStockData, name='stockQuoteJson'),
    url(r'^chart/(?P<ticker>[A-Z]+)/(?P<interval>[a-zA-Z0-9]+)/$', views.getStockDataForCharting, name='stockQuoteChart')
]
