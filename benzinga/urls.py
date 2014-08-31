from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

#from portfolio import views

## this is a hack to get around icompatibe setups between heroku and my IDE
try:
    from benzinga.portfolio import views
except ImportError : 
    from portfolio import  views



from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'benzinga.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', RedirectView.as_view(url='/portfolio' )  , name='index'),
    url(r'^portfolio',  views.UpdatePortfolioView.as_view() , name='portfolio'),
    url(r'^search', views.SearchView.as_view() , name='search') ,
    url(r'^admin/', include(admin.site.urls)),
    
)
