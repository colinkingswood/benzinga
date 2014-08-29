import requests
from django.shortcuts import render
from django.views.generic import ListView
from .models import Purchase, Stock

class PortfolioView(ListView):
    """
    This will be the view to generate the main page - a list of stocks, and a form to buy / sell one
    """  

    
    model = Purchase
    context_object_name = "chosen_stock"
    template_name = "portfolio.html"
#    pagination = 10
    
    
    def get_context_data(self):
        pass
#         response = requests.get(url=model_url, headers=headers , data=payload)
#         return stock 
