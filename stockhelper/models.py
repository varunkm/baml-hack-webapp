from __future__ import unicode_literals
from django.db import models

# Create your models here.
class StockQuote(models.Model):
    company = models.CharField(max_length=10)
    risk = models.CharField(max_length=15)
    openTime = models.DateTimeField()
    highPrice = models.DecimalField(max_digits=12,decimal_places=4)
    lowPrice = models.DecimalField(max_digits=12,decimal_places=4)
    openPrice = models.DecimalField(max_digits=12,decimal_places=4)
    closePrice = models.DecimalField(max_digits=12,decimal_places=4)
    period = models.CharField(max_length=40)
    volume = models.DecimalField(max_digits=14,decimal_places=2)

    def __str__(self):
        rep = '\n'
        rep+= self.company + ' - '+self.period+'\n'
        rep+= str(self.openTime) +'\n'
        rep+= 'H: '+self.highPrice+' L: '+self.lowPrice+' O: '+self.openPrice+' C: '+self.closePrice
        return rep

    def __repr__(self):
        rep = '\n'
        rep+= self.company + ' - '+self.period+'\n'
        rep+= str(self.openTime) +'\n'
        rep+= 'H: '+self.highPrice+' L: '+self.lowPrice+' O: '+self.openPrice+' C: '+self.closePrice
        return rep
class StockQuoteLocal():
    company = models.CharField(max_length=10)
    risk = models.CharField(max_length=15)
    openTime = models.DateTimeField()
    highPrice = models.DecimalField(max_digits=12,decimal_places=4)
    lowPrice = models.DecimalField(max_digits=12,decimal_places=4)
    openPrice = models.DecimalField(max_digits=12,decimal_places=4)
    closePrice = models.DecimalField(max_digits=12,decimal_places=4)
    period = models.CharField(max_length=40)
    volume = models.DecimalField(max_digits=14,decimal_places=2)

    def __str__(self):
        rep = '\n'
        rep+= self.company + ' - '+self.period+'\n'
        rep+= str(self.openTime) +'\n'
        rep+= 'H: '+self.highPrice+' L: '+self.lowPrice+' O: '+self.openPrice+' C: '+self.closePrice
        return rep

    def __repr__(self):
        rep = '\n'
        rep+= self.company + ' - '+self.period+'\n'
        rep+= str(self.openTime) +'\n'
        rep+= 'H: '+self.highPrice+' L: '+self.lowPrice+' O: '+self.openPrice+' C: '+self.closePrice
        return rep
