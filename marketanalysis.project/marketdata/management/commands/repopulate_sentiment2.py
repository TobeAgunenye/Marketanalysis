# repopulate_sentiment2.py

from django.core.management.base import BaseCommand
from marketdata.models import SentimentAnalysis, StockData
from marketdata.views import fetch_news, analyze_sentiment

class Command(BaseCommand):
    help = 'Repopulates the sentiment data with VADER analysis'

    def handle(self, *args, **kwargs):
        # Get all companies from the SentimentAnalysis model
        companies = SentimentAnalysis.objects.values('company').distinct()

        for company in companies:
            print(f"Processing company: {company['company']}")
            articles = fetch_news(company['company'])  # Fetch news articles for the company

            for article in articles:
                text = f"{article.get('title', '')} {article.get('description', '')}"
                sentiment_score, sentiment_label = analyze_sentiment(text)

                # Fetch the StockData instance based on the company name
                stock = StockData.objects.filter(company=company['company']).first()

                if stock:
                    # If the StockData instance exists, update or create SentimentAnalysis record
                    sentiment_data = SentimentAnalysis.objects.filter(company=stock, article_title=article['title']).first()

                    if sentiment_data:
                        # Update existing sentiment data
                        sentiment_data.sentiment_score = sentiment_score
                        sentiment_data.sentiment_label = sentiment_label
                        sentiment_data.save()
                        print(f"Updated sentiment data for article: {article['title']}")
                    else:
                        # Create new SentimentAnalysis record
                        SentimentAnalysis.objects.create(
                            company=stock,  # Assign the StockData instance here
                            sentiment_score=sentiment_score,
                            sentiment_label=sentiment_label,
                            article_title=article['title'],
                            source=article['source']['name']
                        )
                        print(f"Created new sentiment data for article: {article['title']}")
                else:
                    print(f"Stock data not found for {company['company']}")

        print("Sentiment data repopulated successfully.")