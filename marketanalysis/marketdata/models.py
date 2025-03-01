from django.db import models


# Model to Store Financial Data
class MarketData(models.Model):
    company_name = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=10)
    stock_price = models.FloatField()
    market_cap = models.BigIntegerField(null=True, blank=True)
    date_collected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.stock_symbol}) - {self.stock_price}"

# Model to Store Twitter Sentiment Data
class SentimentAnalysis(models.Model):
    company = models.ForeignKey(MarketData, on_delete=models.CASCADE)
    tweet_text = models.TextField()
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=10, choices=[('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')])
    date_collected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.company_name}: {self.sentiment_label}"

# Model to Store AI Predictions
class MarketPrediction(models.Model):
    company = models.ForeignKey(MarketData, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    confidence_score = models.FloatField()
    prediction_date = models.DateTimeField()

    def __str__(self):
        return f"{self.company.company_name} - Predicted Price: {self.predicted_price}"

# Create your models here.
