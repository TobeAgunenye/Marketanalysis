from django.db import models

class StockData(models.Model):
    company = models.CharField(
        max_length=10,
        choices=[
            ('AAPL', 'Apple'),
            ('AMZN', 'Amazon'),
            ('GOOG', 'Google'),
            ('TSLA', 'Tesla')
        ],
        default='AAPL'  # Temporary default
    )
    date = models.DateField()
    open_price = models.FloatField(default=0.0)
    high_price = models.FloatField(default=0.0)
    low_price = models.FloatField(default=0.0)
    close_price = models.FloatField(default=0.0)  # Added default
    volume = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'date'])
        ]
        unique_together = ('company', 'date')

    def __str__(self):
        return f"{self.company} - {self.date}"


# Model to Store Twitter Sentiment Data
class SentimentAnalysis(models.Model):
    company = models.ForeignKey(StockData, on_delete=models.CASCADE)
    tweet_text = models.TextField()
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=10, choices=[('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')])
    date_collected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.company_name}: {self.sentiment_label}"

# Model to Store AI Predictions
class MarketPrediction(models.Model):
    company = models.ForeignKey(StockData, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    confidence_score = models.FloatField()
    prediction_date = models.DateTimeField()

    def __str__(self):
        return f"{self.company.company_name} - Predicted Price: {self.predicted_price}"

# Create your models here.
