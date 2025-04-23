from rest_framework import serializers
from .models import StockData, MarketPrediction, SentimentAnalysis

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'

class MarketPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrediction
        fields = ['company', 'predicted_price', 'confidence_score', 'prediction_date']


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    # Add the company name to the response (instead of just the ID)
    company_name = serializers.CharField(source='company.company', read_only=True)

    class Meta:
        model = SentimentAnalysis
        fields = ['id', 'company_name', 'sentiment_score', 'sentiment_label', 'article_title', 'source']