import requests
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Stock(models.Model) :
    name = models.CharField(max_length=100) ## 69 chars seemed to be the biggest, so 100 should safely cover it 
    symbol    =  models.CharField(max_length=5 , unique=True)  
    ask    = models.DecimalField(max_digits=8, decimal_places=2) 
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return self.symbol
    

    @staticmethod
    def get_from_symbol(symbol=None):
        """
        This will send a json request to teh benzinga servers to get a stock detail
        """
        url = "http://data.benzinga.com/stock/"    
        if not symbol: 
            return None
        
        ## contact the benzinga server for the stock details 
        response = requests.get(url + symbol)
        if response.status_code == 200 :
            json = response.json()
            
            # check json for errors
            if 'status' in json and json['status'] == "error":
                raise Exception(json['msg']) 
        try :
            stock = Stock.objects.get(symbol=json['symbol'])
        except ObjectDoesNotExist as e :
            stock = Stock(name=json['name'], symbol=json['symbol'])
       
        # update to latest prices
        stock.ask = json['ask']
        stock.bid = json['bid']
        stock.save() 
        return stock
    
class Purchase(models.Model):
    stock = models.ForeignKey(Stock) 
    quantity = models.PositiveIntegerField()
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return self.stock.symbol
       
