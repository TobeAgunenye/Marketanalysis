from django.contrib import admin
from .models import MarketData, SentimentAnalysis, MarketPrediction

admin.site.register(MarketData)
admin.site.register(SentimentAnalysis)
admin.site.register(MarketPrediction)
# Register your models here.
