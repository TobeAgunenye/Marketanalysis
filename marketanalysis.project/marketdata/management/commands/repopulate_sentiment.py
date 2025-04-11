# from django.core.management.base import BaseCommand
# from marketdata.models import SentimentAnalysis, StockData
# from marketdata.views import fetch_news
# from textblob import TextBlob

# class Command(BaseCommand):
#     help = 'Repopulates sentiment data for all companies with articles and sentiment analysis'

#     def handle(self, *args, **kwargs):
#         companies = ['AAPL', 'AMZN', 'TSLA', 'GOOG']

#         for company_name in companies:
#             articles = fetch_news(company_name)  # Fetch articles from the NewsAPI

#             if articles:
#                 # Get the StockData instance for the company
#                 stock = StockData.objects.filter(company=company_name).first()
                
#                 if not stock:
#                     self.stdout.write(self.style.WARNING(f"Stock data not found for {company_name}. Skipping..."))
#                     continue

#                 for article in articles:
#                     # Safely handle None values for title and description
#                     title = article.get('title', 'No title available')  # Default to 'No title available' if None
#                     description = article.get('description', '')  # Default to empty string if None

#                     # Skip articles with missing title or description
#                     if not title or not description:
#                         self.stdout.write(self.style.WARNING(f"Skipping article due to missing title or description: {article}"))
#                         continue  # Skip this article if title or description is missing

#                     # Concatenate title and description for sentiment analysis
#                     text = str(title) + " " + str(description)  # Ensure both are strings
                    
#                     # Perform sentiment analysis on the concatenated text
#                     sentiment_score = TextBlob(text).sentiment.polarity  # Sentiment score from -1 to 1
#                     sentiment_label = 'neutral'

#                     if sentiment_score > 0:
#                         sentiment_label = 'positive'
#                     elif sentiment_score < 0:
#                         sentiment_label = 'negative'

#                     # Save the sentiment analysis data to the database
#                     SentimentAnalysis.objects.create(
#                         company=stock,  # Assign the actual StockData instance here
#                         sentiment_score=sentiment_score,
#                         sentiment_label=sentiment_label,
#                         source=article.get('source', {}).get('name', 'Unknown'),
#                         article_title=title
#                     )

#                 self.stdout.write(self.style.SUCCESS(f"Repopulated sentiment data for {company_name}"))
#             else:
#                 self.stdout.write(self.style.WARNING(f"No articles found for {company_name}"))

#         self.stdout.write(self.style.SUCCESS("Repopulation of sentiment data completed."))


from django.core.management.base import BaseCommand
from marketdata.models import SentimentAnalysis, StockData
from marketdata.views import fetch_news
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # Import VADER

class Command(BaseCommand):
    help = 'Repopulates sentiment data for all companies with articles and sentiment analysis using VADER'

    def handle(self, *args, **kwargs):
        companies = ['AAPL', 'AMZN', 'TSLA', 'GOOG']

        # Initialize VADER SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()

        for company_name in companies:
            articles = fetch_news(company_name)  # Fetch articles from the NewsAPI

            if articles:
                # Get the StockData instance for the company
                stock = StockData.objects.filter(company=company_name).first()
                
                if not stock:
                    self.stdout.write(self.style.WARNING(f"Stock data not found for {company_name}. Skipping..."))
                    continue

                for article in articles:
                    # Safely handle None values for title and description
                    title = article.get('title', 'No title available')  # Default to 'No title available' if None
                    description = article.get('description', '')  # Default to empty string if None

                    # Skip articles with missing title or description
                    if not title or not description:
                        self.stdout.write(self.style.WARNING(f"Skipping article due to missing title or description: {article}"))
                        continue  # Skip this article if title or description is missing

                    # Concatenate title and description for sentiment analysis
                    text = str(title) + " " + str(description)  # Ensure both are strings
                    
                    # Perform sentiment analysis with VADER
                    sentiment_score = analyzer.polarity_scores(text)['compound']  # Get compound score from VADER
                    sentiment_label = 'neutral'

                    if sentiment_score > 0:
                        sentiment_label = 'positive'
                    elif sentiment_score < 0:
                        sentiment_label = 'negative'

                    # Save the sentiment analysis data to the database
                    SentimentAnalysis.objects.create(
                        company=stock,  # Assign the actual StockData instance here
                        sentiment_score=sentiment_score,
                        sentiment_label=sentiment_label,
                        source=article.get('source', {}).get('name', 'Unknown'),
                        article_title=title
                    )

                self.stdout.write(self.style.SUCCESS(f"Repopulated sentiment data for {company_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"No articles found for {company_name}"))

        self.stdout.write(self.style.SUCCESS("Repopulation of sentiment data completed."))