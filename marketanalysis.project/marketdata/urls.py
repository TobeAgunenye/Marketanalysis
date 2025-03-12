from django.urls import path
from django.urls import path, include, re_path
from .views import StockDataAPIView
from django.http import HttpResponse, HttpResponseRedirect


urlpatterns = [
    path('api/stock-data/', StockDataAPIView.as_view(), name='stock-data'),
    re_path(r'^$', lambda request: HttpResponseRedirect('/api/stock-data/')),

]
