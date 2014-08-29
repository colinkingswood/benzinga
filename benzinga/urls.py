from django.conf.urls import patterns, include, url
#from portfolio import views

## this is a hack to get around icompatibe stups between heroku and my IDE
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
    url(r'^$',  views.PortfolioView.as_view() , name='portfolio'),
    url(r'^portfolio$',  views.PortfolioView.as_view() , name='portfolio'),
    url(r'^admin/', include(admin.site.urls)),
    
)
