from django.core.management.base import BaseCommand
from marketdata.models import SentimentAnalysis
from marketdata.views import fetch_news

class Command(BaseCommand):
    help = 'Updates article titles in the SentimentAnalysis model'

    def handle(self, *args, **kwargs):
        # Check if there are any records with null article titles
        missing_titles = SentimentAnalysis.objects.filter(article_title__isnull=True)
        self.stdout.write(self.style.SUCCESS(f"Found {missing_titles.count()} records with no article title."))

        # Loop through all records with no article title
        for sentiment in missing_titles:
            company = sentiment.company.company  # Get company name from the ForeignKey relationship
            articles = fetch_news(company)  # Fetch news articles for the company

            # If articles exist, update the sentiment data
            if articles:
                sentiment.article_title = articles[0].get('title', 'No title available')  # Get the first article's title
                sentiment.save()
                self.stdout.write(self.style.SUCCESS(f"Updated title for {company}: {sentiment.article_title}"))
            else:
                self.stdout.write(self.style.WARNING(f"No articles found for {company}"))
        
        self.stdout.write(self.style.SUCCESS("Article title update completed."))