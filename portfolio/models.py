from django.db import models

class Stock(models.Model) :
    name = models.CharField() 
    symbol    =  models.CharField(max_length=5)  
    ask    = models.DecimalField(max_digits=8, decimal_places=2) 
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return self.symbol

class Purchase(models.Model):
    stock = models.ForeignKey(Stock) 
    quantity = models.PositiveIntegerField()
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return self.stock