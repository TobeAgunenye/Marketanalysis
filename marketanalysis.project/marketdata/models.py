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
    company = models.ForeignKey(StockData, on_delete=models.CASCADE)  # Link to the StockData model
    sentiment_score = models.FloatField()  # Sentiment polarity score (from TextBlob or another sentiment library)
    sentiment_label = models.CharField(
        max_length=10,
        choices=[('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')]
    )  # Sentiment label (Positive, Neutral, Negative)
    article_title = models.CharField(max_length=255, null=True, blank=True)  # Add titl
    source = models.CharField(max_length=255, blank=True, null=True)  # Optional field to store the source of the sentiment data (e.g., NewsAPI or Twitter)
    date_collected = models.DateTimeField(auto_now_add=True)  # When the sentiment data was collected
    

    def __str__(self):
        return f"{self.company.company} - {self.sentiment_label} ({self.sentiment_score}) ({self.article_title})"

# Model to Store AI Predictions
class MarketPrediction(models.Model):
    company = models.ForeignKey(StockData, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    confidence_score = models.FloatField()
    prediction_date = models.DateTimeField()

    def __str__(self):
        return f"{self.company.company_name} - Predicted Price: {self.predicted_price}"

# Create your models here.
