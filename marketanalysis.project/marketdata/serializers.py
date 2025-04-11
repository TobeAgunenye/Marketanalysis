from rest_framework import serializers
from .models import StockData
from .models import SentimentAnalysis

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    # Add the company name to the response (instead of just the ID)
    company_name = serializers.CharField(source='company.company', read_only=True)

    class Meta:
        model = SentimentAnalysis
        fields = ['id', 'company_name', 'sentiment_score', 'sentiment_label', 'article_title', 'source']