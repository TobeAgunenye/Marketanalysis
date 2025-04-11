from django.urls import path
from django.urls import path, include, re_path
from .views import StockDataAPIView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from . import views 


urlpatterns = [
    path('api/stock-data/', StockDataAPIView.as_view(), name='stock-data'),  
    path('api/sentiment/<str:company>/', views.SentimentAnalysisAPIView.as_view(), name='sentiment-analysis-company'),
    path('api/sentiment/<str:company>/', views.sentiment_analysis, name='sentiment_analysis'),
    path('api/predict/<str:company>/', views.update_predictions, name='update_predictions'),
]
