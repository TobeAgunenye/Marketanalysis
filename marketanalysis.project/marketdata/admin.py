from django.contrib import admin
from .models import StockData, SentimentAnalysis, MarketPrediction

admin.site.register(StockData)
admin.site.register(SentimentAnalysis)
admin.site.register(MarketPrediction)
# Register your models here.
