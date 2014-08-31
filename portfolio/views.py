from decimal import Decimal
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, RedirectView, FormView, View
from django.core.urlresolvers import reverse, NoReverseMatch
from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe  
from django.db.models import Sum

from .models import Purchase, Stock
from .forms import PurchaseForm 
 
 
class SearchView(View):
    """
    This will redirect to the normal view with the querystring added
    """
    query_string = False
    
    def get(self, request, *args, **kwargs) :
        search_str = self.request.GET.__getitem__('search')
        url = "portfolio?selected=%s" % search_str
        return http.HttpResponseRedirect(url)



class UpdatePortfolioView(FormView):
    """
    This will be the main view that processes the POST reqests (buy and sell), then generates the page
    """
    form_class = PurchaseForm
    template_name = 'portfolio.html'


    def get_initial(self):
        """
        I want to populate a hidden form field with the selected stock
        """
        if self.request.REQUEST.__contains__('selected') : 
             symbol = self.request.REQUEST.__getitem__('selected')
             initial = {} 
             try:
                 initial['stock'] = Stock.get_from_symbol(symbol) 
             except : 
                  pass
             return initial 
 


    def get(self, request, *args, **kwargs):
        """
        Override the get method, and set a sessoon cookie with the amount
        """
        if self.request.session.__contains__('money'):
            pass
        else : 
            # no money, set it $100,000.00
            self.request.session['money'] = '100000.00'  
        return super(UpdatePortfolioView, self).get( request, *args, **kwargs) 




    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        #set the sucess url here - to same page
        
        try:
            self.success_url = self.request.META['HTTP_REFERER']
        except  Exception as e : 
            self.success_url = reverse("portfolio")
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)
    
    

    def form_valid(self, form, request ):
        ##  do some checks here, for money and amount, not the best place, 
        ## ideally I would override the is_valid in forms, but that will probably take me too long. 
        cd = form.cleaned_data  
        buy_or_sell = request.POST.get('buy_or_sell')
        
        if buy_or_sell == 'buy' : 
            return self.buy_stock(form, cd)
        elif buy_or_sell == 'sell':
            return self.sell_stock(form , cd)
            
    
     
            
    def buy_stock(self, form, cleaned_data):
              
        # first get the amount of money left
        amount_left = Decimal(self.request.session['money'])
        
        # check we have enough money 
        total_cost = Decimal(cleaned_data['quantity']) * Decimal(cleaned_data['stock'].ask)
        if  total_cost > amount_left: 
            ## return errors
            form._errors = {'quantity': mark_safe("You don't have enough money<br>")}
            return self.form_invalid(form)
        
        else:
            # create the purchase object in the database
            purchase = Purchase(
                     quantity = cleaned_data['quantity'],
                     stock = cleaned_data['stock'] ,
                     price_paid = cleaned_data['stock'].ask
                     ) 
            purchase.save() 
            self.request.session['money'] = str(amount_left - total_cost)
            return super(UpdatePortfolioView, self).form_valid(form) 


    def sell_stock(self, form, cleaned_data):
              
        stock = cleaned_data['stock'] 
        quantity_to_sell = cleaned_data['quantity']
             
        # first get the amount of money left, 
        purchase_qs = Purchase.objects.filter(stock__symbol=stock.symbol).order_by('quantity')
        stock_quantity  = purchase_qs.aggregate(Sum('quantity'))['quantity__sum']
        
        if  quantity_to_sell > stock_quantity: 
            form._errors = {'quantity': mark_safe("You don't have enough stock to sell<br>")}
            return self.form_invalid(form)
    
        else:
            # I assume that we may have multiple purchases of the same stock
            # Go through list of stocks, deleteing, until we have reached the sell quantity
            
            sold_price = quantity_to_sell * stock.bid
            for purchase in purchase_qs : 
                
                if quantity_to_sell < 0 : 
                    break
                
                if purchase.quantity > quantity_to_sell:
                    purchase.quantity = purchase.quantity - quantity_to_sell
                    purchase.save()
                    quantity_to_sell = 0
                     
                elif purchase.quantity <= quantity_to_sell : 
                    quantity_to_sell = quantity_to_sell - purchase.quantity 
                    purchase.delete()
            
            amount_left = Decimal(self.request.session['money'])
            self.request.session['money'] = str(amount_left + sold_price)
            return super(UpdatePortfolioView, self).form_valid(form)  




    def get_context_data(self,  **kwargs):
        context = super(UpdatePortfolioView, self).get_context_data(**kwargs)
        context['purchase_list'] = Purchase.objects.all() # filter(session=session) 
        if self.request.REQUEST.__contains__('selected'): 
            symbol = self.request.REQUEST.__getitem__('selected')
            try :  
                stock = Stock.get_from_symbol(symbol)
                context['stock'] = stock  
    
            except Exception as e : 
                context['stock_errors'] = "Problem creating stock from json data: " + e.__str__()
        
        context['money'] = self.request.session['money']
            
        return context
        
